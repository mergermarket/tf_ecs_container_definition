import json
import os
import tempfile
import shutil
from subprocess import check_call


class TerraformHelper:
    def __init__(self, terraform_root_path, vars, varfiles, env):
        self.terraform_root_path = terraform_root_path
        self.vars = vars
        self.varfiles = varfiles
        self.env = env

    def run_terraform(self):
        def _flatten_list(l):
            return sum(l, [])

        args = [
            '-refresh=false'
            ]

        args += _flatten_list(
                    [['-var', '{}={}'.format(key, val)]
                        for key, val in self.vars.items()]
                )

        args += _flatten_list([['-var-file', f] for f in self.varfiles])

        tmpdir = tempfile.mkdtemp()
        tfstate_file = os.path.join(tmpdir, 'terraform.tfstate')
        args += [
            '-state={}'.format(tfstate_file),
        ]
        args

        check_call_env = os.environ.copy()
        check_call_env.update(self.env)

        check_call(
                ['terraform', 'get'] + [self.terraform_root_path ],
                env=check_call_env)
        check_call(
                ['terraform', 'apply'] + args +
                [ self.terraform_root_path ],
                env=check_call_env)
        with open(tfstate_file) as tfstate_file:
            tfstate = json.load(tfstate_file)

        shutil.rmtree(tmpdir)

        self.tfstate = tfstate

        return tfstate

    def get_resource_from_module(self, module, resource):
        for m in self.tfstate['modules']:
            if module in m['path']:
                if resource in m['resources']:
                    return m['resources'][resource]

    def get_output_from_module(self, module, output):
        for m in self.tfstate['modules']:
            if module in m['path']:
                if output in m['outputs']:
                    return m['outputs'][output]['value']
        return None
