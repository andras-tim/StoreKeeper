import unittest
from test.Mock.ConfigMock import ConfigMock
from app.config import Config, CircularDependency


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.mocked_config_variables = Config.config_variables
        self.mocked_config_variables["BASEDIR"] = "/test"

    def test_used_config(self):
        config = Config.read(config_reader=ConfigMock('ProductionConfig').config_reader)
        self.assertEqual("Production", config.DebugId)

        config = Config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader)
        self.assertEqual("Development", config.DebugId)

        config = Config.read(config_reader=ConfigMock('TestingConfig').config_reader)
        self.assertEqual("Testing", config.DebugId)

    def test_config_iterator(self):
        config = Config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        self.assertIn("App", config)
        self.assertIn("MIGRATE_REPO_PATH", config.App)

    def test_config_key_getter(self):
        config = Config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        self.assertIn("MIGRATE_REPO_PATH", config["App"])

    def test_single_level_inheritance(self):
        config = Config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader)
        self.assertIn("MIGRATE_REPO_PATH", config.App)
        self.assertIn("SqlAlchemy", config)

    def test_multi_level_inheritance(self):
        config = Config.read(config_reader=ConfigMock('DependencyTopConfig').config_reader)
        self.assertEqual("DependencyTop", config.DebugId)
        self.assertDictEqual({
            1: "Top",
            2: "Middle",
            3: "Bottom",
        }, config.DependencyLevel.get_dict())

    def test_single_level_circular_dependency_in_inheritance(self):
        try:
            Config.read(config_reader=ConfigMock('MinimalCircularConfig').config_reader)
        except Exception as e:
            self.assertIsInstance(e, CircularDependency)

    def test_multi_level_circular_dependency_in__inheritance(self):
        try:
            Config.read(config_reader=ConfigMock('MultiCircularConfigTop').config_reader)
        except Exception as e:
            self.assertIsInstance(e, CircularDependency)

    def test_magic_attribute_not_exits_exception(self):
        try:
            Config.read(config_reader=ConfigMock('ProductionConfig').config_reader).not_exited_attribute
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def test_substitution(self):
        config = Config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader,
                             config_variables=self.mocked_config_variables)
        self.assertNotIn("$BASE", config.App.MIGRATE_REPO_PATH)
        self.assertEqual("/test/db_repository", config.App.MIGRATE_REPO_PATH)

    def test_config_validity(self):
        config = Config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader,
                             config_variables=self.mocked_config_variables)
        self.assertDictEqual({
            "DebugId": "Development",
            "App": {
                "MIGRATE_REPO_PATH": "/test/db_repository",
            },
            "Flask": {
                "SERVER_NAME": "0.0.0.0:8000",
                "STATIC_FOLDER": "/test",
                "DEBUG": True,
                "TESTING": False,
            },
            "SqlAlchemy": {
                "SQLALCHEMY_DATABASE_URI": "sqlite:///test/app.sqlite",
            },
        }, config.get_dict())
