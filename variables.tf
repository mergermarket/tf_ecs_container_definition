variable "container_name" {
  description = "The docker image to use"
}

variable "image" {
  description = "The docker image to use"
}

variable "cpu" {
  description = "The CPU limit for this container definition"
  default     = "256"
}

variable "memory" {
  description = "The memory limit for this container definition"
  default     = "256"
}


variable "container_port" {
  description = "App port to expose in the container"
  default     = "8080"
}

variable "container_env" {
  description = "Environment variables for this container"
  type        = "map"
}

variable "metadata" {
  description = "Metadata for this image. Will be passed as environment variables and labels"
  type        = "map"
}


