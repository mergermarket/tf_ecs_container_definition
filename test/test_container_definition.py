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

    def tearDown(self):
        self.terraform.cleanup()

    def test_container_definition_is_a_valid_json(self):
        # when
        vars = {
            'container_name': self.name,
            'image': '123',
        }
        self.terraform.do_apply(vars)

        # then
        container_definitions_json = self.terraform.get_output(
            output_name='rendered',
        )
        assert container_definitions_json != ""
        try:
            json.loads(container_definitions_json)
        except ValueError:
            self.fail("Container definition is not a valid json")
