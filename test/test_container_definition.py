import unittest
import os
import time
import json
from terraform_helper import TerraformHelper


REGION = 'eu-west-1'

cwd = os.getcwd()


class TestContainerDefinition(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_container_definition_is_a_valid_json(self):
        # when
        name = 'test-' + str(int(time.time() * 1000))

        terraform = TerraformHelper(
            'test/infra',
            {
                'name': name,
                'metadata': '{}',
                'container_env': '{}',
                'image': '123',
            }, [], [])

        terraform.run_terraform()

        # then
        container_definitions_json = terraform.get_output_from_module(
            'container_definition', 'rendered'
        )
        assert container_definitions_json != ""
        try:
            json.loads(container_definitions_json)
        except ValueError:
            self.fail("Container definition is not a valid json")
