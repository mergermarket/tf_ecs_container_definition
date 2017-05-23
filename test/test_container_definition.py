import unittest
import os
import time
import tempfile
import shutil
import json

from subprocess import check_call, check_output


REGION = 'eu-west-1'

cwd = os.getcwd()


class TestContainerDefinition(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.module_path = os.getcwd()

        check_call([
            'terraform', 'get', self.module_path
            ],
            cwd=self.workdir)

    def tearDown(self):
        check_call(
            ['terraform', 'destroy', '-force'] +
            self.last_args +
            [self.module_path],
            cwd=self.workdir)

        if os.path.isdir(self.workdir):
            shutil.rmtree(self.workdir)

    def _apply_and_parse(self, vars, varsmap={}):
        varsmap_file = os.path.join(self.workdir, 'varsmap.json')
        with open(varsmap_file, 'w') as f:
            f.write(json.dumps(varsmap))

        args = sum([
            ['-var', '{}={}'.format(key, val)]
            for key, val in vars.items()
            ], [])

        args += ['-var-file', varsmap_file]

        self.last_args = args

        check_call([
            'terraform', 'apply',
            '-no-color'
            ] + args +
            [self.module_path],
            cwd=self.workdir
        )

        output = check_output([
            'terraform', 'output', '-json', 'rendered'],
            cwd=self.workdir).decode('utf8')

        parsed_output = json.loads(output)["value"]
        parsed_definition = json.loads(parsed_output)
        return parsed_definition

    def test_is_a_valid_json(self):
        # Given
        vars = {
            'name': 'test-' + str(int(time.time() * 1000)),
            'image': '123',
            'cpu': 1024,
            'memory': 1024,
            'container_port': 8001
        }
        varsmap = {}

        # when
        definition = self._apply_and_parse(vars, varsmap)

        # then
        assert definition['name'] == vars['name']
        assert definition['image'] == '123'
        assert definition['cpu'] == 1024
        assert definition['memory'] == 1024
        assert definition['essential']

        assert {'containerPort': 8001} in definition['portMappings']

    def test_inserts_common_vars(self):
        # Given
        vars = {
            'name': 'test-' + str(int(time.time() * 1000)),
            'image': '123',
            'cpu': 1024,
            'memory': 1024,
            'container_port': 8001
        }
        varsmap = {}

        # when
        definition = self._apply_and_parse(vars, varsmap)

        # then
        assert {
            'name': 'LOGSPOUT_CLOUDWATCHLOGS_LOG_GROUP_STDOUT',
            'value': '{}-stdout'.format(vars['name'])
            } in definition['environment']
        assert {
            'name': 'LOGSPOUT_CLOUDWATCHLOGS_LOG_GROUP_STDERR',
            'value': '{}-stderr'.format(vars['name'])
            } in definition['environment']
        assert {
            'name': 'STATSD_HOST',
            'value': '172.17.42.1',
            } in definition['environment']
        assert {
            'name': 'STATSD_PORT',
            'value': '8125',
            } in definition['environment']
        assert {
            'name': 'STATSD_ENABLED',
            'value': 'true',
            } in definition['environment']

    def test_include_image_container_env(self):
        # Given
        vars = {
            'name': 'test-' + str(int(time.time() * 1000)),
            'image': '123',
            'cpu': 1024,
            'memory': 1024,
            'container_port': 8001
        }
        varsmap = {}

        # when
        definition = self._apply_and_parse(vars, varsmap)

        # then
        assert {
            'name': 'DOCKER_IMAGE',
            'value': '123'
            } in definition['environment']

    def test_metadata(self):
        # Given
        vars = {
            'name': 'test-' + str(int(time.time() * 1000)),
            'image': '123',
            'cpu': 1024,
            'memory': 1024,
            'container_port': 8001
        }
        varsmap = {
            'metadata': {
                'label_key_1': 'label_value_1',
                'label_key_2': 'label_value_2',
            }
        }

        # when
        definition = self._apply_and_parse(vars, varsmap)

        # then
        assert {
            'name': 'LABEL_KEY_1',
            'value': 'label_value_1'
            } in definition['environment']
        assert {
            'name': 'LABEL_KEY_2',
            'value': 'label_value_2'
            } in definition['environment']

        for key in varsmap['metadata']:
            assert varsmap['metadata'][key] in definition['dockerLabels'][key]

    def test_container_env(self):
        # given
        vars = {
            'name': 'test-' + str(int(time.time() * 1000)),
            'image': '123',
            'cpu': 1024,
            'memory': 1024,
            'container_port': 8001
        }
        varsmap = {
            'container_env': {
                'VAR1': 'value_1',
                'VAR2': 'value_2',
            }
        }

        # when
        definition = self._apply_and_parse(vars, varsmap)

        # then
        assert {
            'name': 'VAR1',
            'value': 'value_1'
            } in definition['environment']
        assert {
            'name': 'VAR2',
            'value': 'value_2'
            } in definition['environment']
