# container definition template mapping
data "template_file" "container_definitions" {
  template = "${file("${path.module}/container_definition.json.tmpl")}"

  vars {
    image              = "${var.image}"
    container_name     = "${var.name}"
    container_port     = "${var.container_port}"
    cpu                = "${var.cpu}"
    mem                = "${var.memory}"
    container_env      = "${data.external.encode_env.result["env"]}"
    labels             = "${jsonencode(var.labels)}"
    nofile_soft_ulimit = "${var.nofile_soft_ulimit}"

    mountpoint_sourceVolume  = "${lookup(var.mountpoint, "sourceVolume", "none")}"
    mountpoint_containerPath = "${lookup(var.mountpoint, "containerPath", "none")}"
    mountpoint_readOnly      = "${lookup(var.mountpoint, "readOnly", false)}"
  }
}

data "external" "encode_env" {
  program = [
    "python", "-c", <<END
import json
from sys import stdin
terraform_input = json.loads(stdin.read())
env = json.loads(terraform_input["env"])
metadata = {
  key.upper(): value
  for key, value
  in json.loads(terraform_input["metadata"]).items()
}
output = [
  {"name": key, "value": value}
  for key, value
  in list(env.items()) + list(metadata.items())
]
print(json.dumps({"env": json.dumps(output)}))
END
  ]

  query = {
    env      = "${jsonencode(var.container_env)}",
    metadata = "${jsonencode(var.metadata)}"
  }
}
