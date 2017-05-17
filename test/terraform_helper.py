import json
import os
import tempfile
import shutil
import subprocess
import atexit


class TerraformHelper:
    def __init__(self, tfdir, env=[]):
        self.terraform_root_path = os.path.realpath(tfdir)
        self.env = env
        self.tmpdir = tempfile.mkdtemp()
        self.tfstate_file = os.path.join(self.tmpdir, 'terraform.tfstate')
        atexit.register(self.cleanup)

    def do_get(self):
        check_call_env = os.environ.copy()
        check_call_env.update(self.env)

        self.last_output = subprocess.check_output(
                ['terraform', 'get'] + [self.terraform_root_path],
                stderr=subprocess.STDOUT,
                cwd=self.tmpdir,
                env=check_call_env)

        return self.last_output

    def do_apply(self, vars, varfiles=[]):
        def _flatten_list(l):
            return sum(l, [])

        args = [
            '-refresh=false'
            ]

        args += _flatten_list(
                    [['-var', '{}={}'.format(key, val)]
                        for key, val in vars.items()]
                )

        args += _flatten_list([['-var-file', f] for f in varfiles])

        check_call_env = os.environ.copy()
        check_call_env.update(self.env)

        self.last_output = subprocess.check_output(
                ['terraform', 'apply'] +
                args +
                [self.terraform_root_path],
                cwd=self.tmpdir,
                env=check_call_env)

        return self.last_output

    def tfstate(self):
        with open(self.tfstate_file) as tfstate_file:
            return json.load(tfstate_file)

    def cleanup(self):
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def get_resource_from_module(self, module, resource):
        for m in self.tfstate()['modules']:
            if module in m['path']:
                if resource in m['resources']:
                    return m['resources'][resource]

    def get_output_from_module(self, module, output):
        for m in self.tfstate()['modules']:
            if module in m['path']:
                if output in m['outputs']:
                    return m['outputs'][output]['value']
        return None
