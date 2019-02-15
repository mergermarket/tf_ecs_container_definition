import json
from sys import stdin

terraform_input = json.loads(stdin.read())
secrets = json.loads(terraform_input.get("secrets", "{}"))
common_secrets = json.loads(terraform_input.get("common_secrets", "{}"))

secrets = [
    {"name": key, "valueFrom": value}
    for key, value
    in list(secrets.items())
]

common_secrets = [
    {"name": key, "valueFrom": value}
    for key, value
    in list(common_secrets.items())
]

output = secrets + common_secrets

print(json.dumps({"secrets": json.dumps(output)}))
