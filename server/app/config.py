import string
import os
import yaml
from collections import Mapping

from app import basedir


class CircularDependency(Exception):
    pass


class ConfigObject(object):
    def __init__(self, config_dict: dict):
        self.__config = config_dict

    def __check(self, name: str):
        if name not in self.__config.keys():
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    def __getattr__(self, name: str):
        self.__check(name)
        if type(self.__config[name]) == dict:
            return ConfigObject(self.__config[name])
        else:
            return self.__config[name]

    def __iter__(self):
        for each in self.__config.keys():
            yield each

    def __getitem__(self, name: str):
        self.__check(name)
        return self.__config[name]

    def get_dict(self)-> dict:
        return self.__config


class Config(object):
    config_variables = {
        'BASEDIR': basedir
    }

    @classmethod
    def read(cls, yaml_config_path: str=None, config_variables: dict=None, config_reader: callable=None)-> ConfigObject:
        if not yaml_config_path:
            yaml_config_path = os.path.join(basedir, "config.yml")
        if not config_variables:
            config_variables = cls.config_variables
        if not config_reader:
            config_reader = cls.__read_file

        raw_config = config_reader(yaml_config_path)

        substituted_config = cls.__substitute_config(raw_config, config_variables)
        parsed_yaml = yaml.load(substituted_config, Loader=yaml.CLoader)

        used_config = parsed_yaml["USED_CONFIG"]
        inherited_config = cls.__inherit_config(parsed_yaml, used_config)

        return ConfigObject(inherited_config[used_config])

    @classmethod
    def __read_file(cls, yaml_config_path: str)-> str:
        with open(yaml_config_path, "r") as fd:
            raw_config = fd.read()
        return raw_config

    @classmethod
    def __substitute_config(cls, raw_config: str, config_variables: dict)-> str:
        config_template = string.Template(raw_config)
        substituted_config = config_template.substitute(config_variables)
        return substituted_config

    @classmethod
    def __inherit_config(cls, parsed_yaml: dict, config_name: str, parent_stack: list=None)-> dict:
        if not parent_stack:
            parent_stack = []
        parent_stack.append(config_name)

        # Has it base?
        if "Base" not in parsed_yaml[config_name].keys():
            return parsed_yaml

        # Skipping circular-dependency
        base_config_name = parsed_yaml[config_name]["Base"]
        if base_config_name in parent_stack:
            raise CircularDependency("Circular dependency detected in config! callstack=%s" %
                                     str(parent_stack + [base_config_name]))
        del parsed_yaml[config_name]["Base"]

        # Get full config with inherited base config
        parsed_yaml = cls.__inherit_config(parsed_yaml, base_config_name, parent_stack)

        # Set base_config based current config
        parsed_yaml[config_name] = cls.__update_dict_recursive(parsed_yaml[base_config_name], parsed_yaml[config_name])

        return parsed_yaml

    @classmethod
    def __update_dict_recursive(cls, base: dict, update: [dict, Mapping])-> dict:
        for k, v in update.items():
            if isinstance(v, Mapping):
                r = cls.__update_dict_recursive(base.get(k, {}), v)
                base[k] = r
            else:
                base[k] = update[k]
        return base
