import json
from sys import stdin

terraform_input = json.loads(stdin.read())

secrets = json.loads(terraform_input["secrets"])

output = [
    {"name": key, "valueFrom": value}
    for key, value
    in list(secrets.items())
]

print(json.dumps({"secrets": json.dumps(output)}))
