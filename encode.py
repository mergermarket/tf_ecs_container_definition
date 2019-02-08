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
