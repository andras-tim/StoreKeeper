from app.modules.example_data import ExampleConfigs as Configs
from test.e2e.base_api_test import CommonApiTest


class TestConfig(CommonApiTest):
    ENDPOINT = '/config'

    def test_config_values(self):
        self.assertApiGet(expected_data=Configs.CONFIG1)
