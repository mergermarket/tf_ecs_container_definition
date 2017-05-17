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
        self.last_apply_args = None
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

        self.last_apply_args = args

        check_call_env = os.environ.copy()
        check_call_env.update(self.env)

        self.last_output = subprocess.check_output(
                ['terraform', 'apply'] +
                args +
                [self.terraform_root_path],
                cwd=self.tmpdir,
                env=check_call_env)

        return self.last_output

    def do_destroy(self):
        if self.last_apply_args is None:
            raise "do_destroy() called without calling do_apply() first."

        check_call_env = os.environ.copy()
        check_call_env.update(self.env)

        self.last_output = subprocess.check_output(
                ['terraform', 'destroy', '-force'] +
                self.last_apply_args +
                [self.terraform_root_path],
                cwd=self.tmpdir,
                env=check_call_env)

        return self.last_output

    def tfstate(self):
        with open(self.tfstate_file) as tfstate_file:
            return json.load(tfstate_file)

    def cleanup(self):
        if os.path.exists(self.tfstate_file):
            self.do_destroy()
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def get_resource_from_module(self, module, resource):
        for m in self.tfstate()['modules']:
            if module in m['path']:
                if resource in m['resources']:
                    return m['resources'][resource]

    def get_output(self, output_name=None, module=None):
        check_call_env = os.environ.copy()
        check_call_env.update(self.env)

        args = []
        if module is not None:
            args += ['-module', module]
        if output_name is not None:
            args += [output_name]
        output = subprocess.check_output(
                ['terraform', 'output', '-json'] + args,
                cwd=self.tmpdir,
                env=check_call_env)

        parsed_output = json.loads(output)
        if output_name is not None:
            return parsed_output["value"]
        else:
            return parsed_output
