# container definition template mapping
data "template_file" "container_definitions" {
  template = "${file("${path.module}/container_definition.json.tmpl")}"

  vars {
    image          = "${var.image}"
    container_name = "${var.container_name}"
    container_port = "${var.container_port}"
    cpu            = "${var.cpu}"
    mem            = "${var.memory}"

    container_env = "${
      join (
        format(",\n      "),
        concat(
          null_resource._jsonencode_container_env.*.triggers.entries,
          null_resource._jsonencode_metadata_env.*.triggers.entries,
          list(jsonencode(
            map(
              "name", "DOCKER_IMAGE",
              "value", var.image,
            )
          ))
        )
      )
    },"

    labels = "${jsonencode(var.metadata)}"
  }

  depends_on = [
    "null_resource._jsonencode_container_env",
    "null_resource._jsonencode_metadata_env"
  ]
}

# Create a json snippet with the list of variables to be passed to
# the container definitions.
#
# It will use a null_resource to generate a list of json encoded
# name-value maps like {"name": "...", "value": "..."}, and then
# we join them in a data template file.
resource "null_resource" "_jsonencode_container_env" {
  triggers {
    entries = "${
      jsonencode(
        map(
          "name", element(keys(var.container_env), count.index),
          "value", element(values(var.container_env), count.index),
          )
      )
    }"
  }

  count = "${length(var.container_env)}"
}

# Json snippet with the list of labels
resource "null_resource" "_jsonencode_metadata_env" {
  triggers {
    entries = "${
      jsonencode(
        map(
          "name", upper(element(keys(var.metadata), count.index)),
          "value", element(values(var.metadata), count.index),
          )
      )
    }"
  }
  count = "${length(var.metadata)}"
}
