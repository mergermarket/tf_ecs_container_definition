`container_definitions` module
-----------------------------

This module should contain the logic that generates our default set of container definitions,
providing the rendered definitions as an output.

Input variables
---------------

 * `container_name` - (string) **REQUIRED** - Name/name prefix to apply to the resources in the module.
 * `image` - (string) **REQUIRED** - The docker image in use
 * `container_port` - (string) OPTIONAL -App port to expose in the container. Default 8080.
 * `cpu`- (string) OPTIONAL -The CPU limit for this container definition
 * `memory`- (string) OPTIONAL - The memory limit for this container definition
 * `env`: (map) OPTIONAL - map with environment variables
 * `metadata`: (map) OPTIONAL - Set of metadata for this container. It will be passed as environment variables (key uppercased) and labels.

Usage
-----

```hcl
module "container_defintions" {
  source = "github.com/mergermarket/tf_ecs_container_definitions"
  
  name           = "some-app"
  image          = "repo/image"
  container_port = "8080"
  cpu            = 1024
  memory         = 256
  
  container_env = {
    VAR1 = "value1"
    VAR2 = "value2"
  }
  
  metadata = {
    "label1" = "label.one"
    "label2" = "label.two"
  } 
}
```

Outputs
-------

 * `rendered`: rendered container definition
