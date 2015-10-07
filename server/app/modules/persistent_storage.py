import json
import fcntl
import os.path
from app import configdir, tempdir


class PersistentStorage:
    STORAGE_PATH = os.path.join(configdir, 'persistent_storage')
    LOCK_PATH = os.path.join(tempdir, 'persistent_storage_locks')

    def __init__(self, storage_name: str='common'):
        self.storage_path = os.path.join(self.STORAGE_PATH, '{}.json'.format(storage_name))
        self.storage_write_lock_path = os.path.join(self.LOCK_PATH, '{}.lck'.format(storage_name))
        self.storage_write_lock_fd = None

        self.__storage = {}

        self.__prepare_directories()
        self.__load()

    def get(self, name: str, default_value=None):
        if name not in self.__storage.keys():
            return default_value
        return self.__storage[name]

    def set(self, name: str, value):
        self.__hold_lock()
        self.__storage[name] = value
        self.__save()
        self.__release_lock()

    def __prepare_directories(self):
        if not os.path.exists(self.STORAGE_PATH):
            os.makedirs(self.STORAGE_PATH)
        if not os.path.exists(self.LOCK_PATH):
            os.makedirs(self.LOCK_PATH)

    def __load(self):
        try:
            with open(self.storage_path, 'r') as fd:
                self.__storage = json.load(fd)
        except FileNotFoundError:
            pass

    def __save(self):
        with open(self.storage_path, 'w') as fd:
            json.dump(self.__storage, fd)

    def __hold_lock(self):
        self.storage_write_lock_fd = open(self.storage_write_lock_path, 'a')
        fcntl.lockf(self.storage_write_lock_fd.fileno(), fcntl.LOCK_EX)

    def __release_lock(self):
        fcntl.lockf(self.storage_write_lock_fd.fileno(), fcntl.LOCK_UN)
        self.storage_write_lock_fd.close()
        self.storage_write_lock_fd = None
