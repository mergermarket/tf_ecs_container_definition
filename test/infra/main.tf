variable "name" {
    description = "used to ensure taskdef updates"
}

module "container_definition" {
  source = "../.."

  container_name = "${var.name}"
  image = "123"

  metadata = {
    env = "aslive"
    team = "x"
  }

  container_env = "${map(
    "FOO", "1",
    "BAR", "2",
  )}"
}

output "container_definition_json" {
    value = "${module.container_definition.rendered}"
}
