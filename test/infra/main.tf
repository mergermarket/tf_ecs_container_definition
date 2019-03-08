# configure provider to not try too hard talking to AWS API
provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

# fixture
module "tf_ecs_container_definition_test" {
  source             = "../.."
  cpu                = "${var.cpu}"
  memory             = "${var.memory}"
  name               = "${var.name}"
  image              = "${var.image}"
  nofile_soft_ulimit = "${var.nofile_soft_ulimit}"
  container_port     = "${var.container_port}"
  labels             = "${var.labels}"
  port_mappings      = "${var.port_mappings}"
  mountpoint         = "${var.mountpoint}"
  container_env      = "${var.container_env}"
  metadata           = "${var.metadata}"
  application_secrets       = "${var.application_secrets}"
  platform_secrets     = "${var.platform_secrets}"
}

variable "name" {}

variable "image" {}

variable "nofile_soft_ulimit" {
  default     = "4096"
}

variable "container_port" { default = "" }
 
variable "labels" { default = {} }
 
variable "port_mappings" { default = "" }
 
variable "mountpoint" { default = {} }
 
variable "container_env" { default = {} }
 
variable "metadata" { default = {} }
 
variable "application_secrets" { default = [] }

variable "platform_secrets" { default = [] }

variable "memory" {}

variable "cpu" {}

output "rendered" {
  value = "${module.tf_ecs_container_definition_test.rendered}"
}
