from app.modules.example_data import ExampleConfigs as Configs
from test.views.base_api_test import CommonApiTest


class TestConfig(CommonApiTest):
    ENDPOINT = '/configs'

    def test_config_values(self):
        self.assertApiGet(expected_data=Configs.CONFIG1)
