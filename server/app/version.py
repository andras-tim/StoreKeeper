import json
import os.path

from app import basedir


class Version:
    __VERSION_JSON_PATH = os.path.abspath(os.path.join(basedir, '..', 'VERSION.json'))

    def __init__(self):
        with open(self.__VERSION_JSON_PATH, 'r') as fd:
            self.__version_array = tuple(json.load(fd))

        version_string_array = [str(v) for v in self.__version_array]
        self.__version = '.'.join(version_string_array[:3])
        self.__release = '-'.join([self.__version] + version_string_array[3:])

    @property
    def version_array(self) -> tuple:
        return self.__version_array

    @property
    def version(self) -> str:
        return self.__version

    @property
    def release(self) -> str:
        return self.__release
