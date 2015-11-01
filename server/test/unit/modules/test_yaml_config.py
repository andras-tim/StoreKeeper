import unittest

from test.unit.mocks.config_mock import ConfigMock
from app.modules.yaml_config import Config, CircularDependencyError


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config('/test/config.yaml', config_variables={'BASEDIR': '/test'})

    def test_used_config(self):
        config = self.config.read(config_reader=ConfigMock('ProductionConfig').config_reader)
        self.assertEqual('Production', config.DebugId)

        config = self.config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader)
        self.assertEqual('Development', config.DebugId)

        config = self.config.read(config_reader=ConfigMock('TestingConfig').config_reader)
        self.assertEqual('Testing', config.DebugId)

    def test_overridden_used_config(self):
        config = self.config.read(config_reader=ConfigMock('ProductionConfig').config_reader,
                                  used_config='DevelopmentConfig')
        self.assertEqual('Development', config.DebugId)

        config = self.config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader,
                                  used_config='TestingConfig')
        self.assertEqual('Testing', config.DebugId)

        config = self.config.read(config_reader=ConfigMock('TestingConfig').config_reader,
                                  used_config='ProductionConfig')
        self.assertEqual('Production', config.DebugId)

    def test_config_iterator(self):
        config = self.config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        self.assertIn('App', config)
        self.assertIn('MIGRATE_REPO_PATH', config.App)

    def test_config_key_getter(self):
        config = self.config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        self.assertIn('MIGRATE_REPO_PATH', config['App'])

    def test_single_level_inheritance(self):
        config = self.config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader)
        self.assertIn('MIGRATE_REPO_PATH', config.App)
        self.assertIn('SqlAlchemy', config)

    def test_multi_level_inheritance(self):
        config = self.config.read(config_reader=ConfigMock('DependencyTopConfig').config_reader)
        self.assertEqual('DependencyTop', config.DebugId)
        self.assertDictEqual({
            1: 'Top',
            2: 'Middle',
            3: 'Bottom',
        }, config.DependencyLevel.get_dict())

    def test_single_level_circular_dependency_in_inheritance(self):
        try:
            self.config.read(config_reader=ConfigMock('MinimalCircularConfig').config_reader)
        except Exception as e:
            self.assertIsInstance(e, CircularDependencyError)

    def test_multi_level_circular_dependency_in__inheritance(self):
        try:
            self.config.read(config_reader=ConfigMock('MultiCircularConfigTop').config_reader)
        except Exception as e:
            self.assertIsInstance(e, CircularDependencyError)

    def test_magic_attribute_not_exits_exception(self):
        try:
            self.config.read(config_reader=ConfigMock('ProductionConfig').config_reader).not_exited_attribute
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def test_substitution(self):
        config = self.config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader)
        self.assertNotIn('$BASE', config.App.MIGRATE_REPO_PATH)
        self.assertEqual('/test/db_repository', config.App.MIGRATE_REPO_PATH)

    def test_config_validity(self):
        config = self.config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader)
        self.assertDictEqual({
            'DebugId': 'Development',
            'App': {
                'MIGRATE_REPO_PATH': '/test/db_repository',
                'UTF8_VALUE': 'Több hűtőházból kértünk színhúst',
            },
            'Flask': {
                'SERVER_NAME': '0.0.0.0:8000',
                'STATIC_FOLDER': '/test',
                'DEBUG': True,
                'TESTING': False,
            },
            'SqlAlchemy': {
                'SQLALCHEMY_DATABASE_URI': 'sqlite:///test/app.sqlite',
            },
        }, config.get_dict())

    def test_str_dump_validity(self):
        config = self.config.read(config_reader=ConfigMock('DevelopmentConfig').config_reader)
        assert """{'App': {'MIGRATE_REPO_PATH': '/test/db_repository',
         'UTF8_VALUE': 'Több hűtőházból kértünk színhúst'},
 'DebugId': 'Development',
 'Flask': {'DEBUG': True,
           'SERVER_NAME': '0.0.0.0:8000',
           'STATIC_FOLDER': '/test',
           'TESTING': False},
 'SqlAlchemy': {'SQLALCHEMY_DATABASE_URI': 'sqlite:///test/app.sqlite'}}""" == str(config)

    def test_can_set_existed_value_by_key(self):
        config = self.config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        config.Flask['STATIC_FOLDER'] = '/new_path'
        assert config.Flask.STATIC_FOLDER == '/new_path'

    def test_can_not_set_existed_value_by_attr(self):
        config = self.config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        config.Flask.STATIC_FOLDER = '/new_path'
        assert config.Flask.STATIC_FOLDER == '/test'

    def test_can_set_not_existed_value_by_key(self):
        config = self.config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        config.Flask['NEW_PROPERTY'] = '/new_path'
        assert 'NEW_PROPERTY' in config.Flask
        assert config.Flask.NEW_PROPERTY == '/new_path'

    def test_can_not_set_not_existed_value_by_attr(self):
        config = self.config.read(config_reader=ConfigMock('DefaultConfig').config_reader)
        config.Flask.NEW_PROPERTY = '/new_path'
        assert 'NEW_PROPERTY' not in config.Flask
