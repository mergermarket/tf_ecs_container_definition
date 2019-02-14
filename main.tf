locals {
    team = "${lookup(var.labels, "team", "")}"
    env = "${lookup(var.labels, "env", "")}"
    component = "${lookup(var.labels, "component", "")}"
}

data "template_file" "container_definitions" {
  template = "${file("${path.module}/container_definition.json.tmpl")}"

  vars {
    image          = "${var.image}"
    container_name = "${var.name}"

    port_mappings = "${
      var.port_mappings == "" ?
        format("[ { \"containerPort\": %s } ]", var.container_port) :
        var.port_mappings
    }"

    cpu                = "${var.cpu}"
    mem                = "${var.memory}"
    container_env      = "${data.external.encode_env.result["env"]}"
    secrets            = "${data.external.encode_secrets.result["secrets"]}"
    labels             = "${jsonencode(var.labels)}"
    nofile_soft_ulimit = "${var.nofile_soft_ulimit}"

    mountpoint_sourceVolume  = "${lookup(var.mountpoint, "sourceVolume", "none")}"
    mountpoint_containerPath = "${lookup(var.mountpoint, "containerPath", "none")}"
    mountpoint_readOnly      = "${lookup(var.mountpoint, "readOnly", false)}"
  }
}

data "external" "encode_env" {
  program = ["python", "${path.module}/encode_env.py"]

  query = {
    env      = "${jsonencode(var.container_env)}",
    metadata = "${jsonencode(var.metadata)}"
  }
}

data "external" "encode_secrets" {
  program = ["python", "${path.module}/encode_secrets.py"]

  query = {
    secrets   = "${jsonencode(zipmap(var.secret_names, data.aws_secretsmanager_secret.secret.*.arn))}"
  }
}

data "aws_secretsmanager_secret" "secret" {
  count = "${length(var.secret_names)}"
  name  = "${local.team}/${local.env}/${local.component}/${element(var.secret_names, count.index)}"
}
