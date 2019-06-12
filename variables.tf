variable "name" {
  description = "Name/name prefix to apply to the resources in the module"
}

variable "image" {
  description = "The docker image to use"
}

variable "cpu" {
  description = "The CPU limit for this container definition"
  default     = "64"
}

variable "memory" {
  description = "The memory limit for this container definition"
  default     = "256"
}

variable "command" {
  description = "The command that is passed to the container"
  type        = "list"
  default     = []
}

variable "nofile_soft_ulimit" {
  description = "The soft ulimit for the number of files in container"
  default     = "4096"
}

variable "container_port" {
  description = "App port to expose in the container"
  default     = "8080"
}

variable "container_env" {
  description = "Environment variables for this container"
  type        = "map"
  default     = {}
}

variable "labels" {
  description = "Labels to be applied to the docker container"
  type        = "map"
  default     = {}
}

variable "metadata" {
  description = "DEPRECATED - values passed to this variable will be ignored"
  type        = "map"
  default     = {}
}

variable "mountpoint" {
  description = "Mountpoint map with 'sourceVolume' and 'containerPath' and 'readOnly' (optional)."
  type        = "map"
  default     = {}
}

variable "port_mappings" {
  description = "JSON document containing an array of port mappings for the container defintion - if set container_port is ignored (optional)."
  default     = ""
  type        = "string"
}

variable "application_secrets" {
  type    = "list"
  default = []
}

variable "platform_secrets" {
  type    = "list"
  default = []
}
