import unittest
import os
import time
import json

from terraform_helper import TerraformHelper


REGION = 'eu-west-1'

cwd = os.getcwd()


class TestContainerDefinition(unittest.TestCase):

    def setUp(self):
        self.terraform = TerraformHelper('.')
        self.terraform.do_get()
        self.name = 'test-' + str(int(time.time() * 1000))
        self.vars = {
            'container_name': self.name,
            'image': '123',
            'cpu': 1024,
            'memory': 1024,
            'container_port': 8001
        }

    def tearDown(self):
        self.terraform.cleanup()

    def _apply_and_parse_output(self, vars, varsmap):
        self.terraform.do_apply(vars=vars, varsmap=varsmap)

        # then
        container_definitions_json = self.terraform.get_output(
            output_name='rendered',
        )
        assert container_definitions_json != ""
        try:
            parsed_output = json.loads(container_definitions_json)
        except ValueError:
            self.fail("Container definition is not a valid json")

        return parsed_output

    def test_is_a_valid_json(self):
        # when
        varsmap = {}
        definition = self._apply_and_parse_output(self.vars, varsmap)

        # then
        assert definition['name'] == self.name
        assert definition['image'] == '123'
        assert definition['cpu'] == 1024
        assert definition['memory'] == 1024
        assert definition['essential']

        assert {'containerPort': 8001} in definition['portMappings']

    def test_inserts_common_vars(self):
        # when
        varsmap = {}
        definition = self._apply_and_parse_output(self.vars, varsmap)

        # then
        assert {
            'name': 'LOGSPOUT_CLOUDWATCHLOGS_LOG_GROUP_STDOUT',
            'value': '{}-stdout'.format(self.name)
            } in definition['environment']
        assert {
            'name': 'LOGSPOUT_CLOUDWATCHLOGS_LOG_GROUP_STDERR',
            'value': '{}-stderr'.format(self.name)
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
        # when
        varsmap = {}
        definition = self._apply_and_parse_output(self.vars, varsmap)
        # then
        assert {
            'name': 'DOCKER_IMAGE',
            'value': '123'
            } in definition['environment']

    def test_metadata(self):
        # when
        varsmap = {
            'metadata': {
                'label_key_1': 'label_value_1',
                'label_key_2': 'label_value_2',
            }
        }

        definition = self._apply_and_parse_output(self.vars, varsmap)

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
        # when
        varsmap = {
            'container_env': {
                'VAR1': 'value_1',
                'VAR2': 'value_2',
            }
        }

        definition = self._apply_and_parse_output(self.vars, varsmap)

        # then
        assert {
            'name': 'VAR1',
            'value': 'value_1'
            } in definition['environment']
        assert {
            'name': 'VAR2',
            'value': 'value_2'
            } in definition['environment']
