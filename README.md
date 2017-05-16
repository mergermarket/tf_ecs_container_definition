`container_definitions` module
-----------------------------

This module should contain the logic that generates our default set of container definitions,
providing the rendered definitions as an output.

Input variables
---------------

 * `image`: The docker image in use
 * `container_port`: App port to expose in the container
 * `cpu`: The CPU limit for this container definition
 * `memory`: The memory limit for this container definition
 * `labels`: Set of docker labels
 * `env`: map with environment variables

Usage
-----

```
module "container_defintions" {
    source = "gihub.com/mergermarket/tf_ecs_container_definitions"

    image          = "repo/image"
    container_port = "8080"
    cpu            = 1024
    memory         = 256
    labels         = {
		"label1" = "label.one"
		"label2" = "label.two"
	}

    env            = {
        VAR1 = "value1"
        VAR2 = "value2"
    }
}

Outputs
-------

 * `rendered`: rendered container definition



