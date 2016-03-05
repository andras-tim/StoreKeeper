import json
import fcntl
import os.path

from app import configdir, tempdir


class PersistentStorage:
    """
    Simple persistent storage

    Use persistent storage context for handle data with proper locking. The storage going to read the persist file when
    enter to the context, and going to save changes when leave it.

    Example usage:
    >>> with PersistentStorage(name='fruits') as storage:
    ...     bar_value = storage.get('orange', default=12)
    ...     storage.set('apple', 20)
    """

    STORAGE_PATH = os.path.join(configdir, 'persistent_storage')
    LOCK_PATH = os.path.join(tempdir, 'persistent_storage_locks')

    def __init__(self, name: str= 'common'):
        self.__json_file_path = os.path.join(self.STORAGE_PATH, '{}.json'.format(name))
        self.__lock_file_path = os.path.join(self.LOCK_PATH, '{}.lck'.format(name))
        self.__lock_fd = None

        self.__storage = {}
        self.__dirty = False

        self.__prepare_directories()

    def __enter__(self) -> 'PersistentStorage':
        self.__hold_lock()
        self.__load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__dirty:
            self.__save()
        self.__release_lock()

    def get(self, name: str, default=None):
        return self.__storage.get(name, default)

    def set(self, name: str, value):
        self.__storage[name] = value
        self.__dirty = True

    def __prepare_directories(self):
        if not os.path.exists(self.STORAGE_PATH):
            os.makedirs(self.STORAGE_PATH)
        if not os.path.exists(self.LOCK_PATH):
            os.makedirs(self.LOCK_PATH)

    def __load(self):
        try:
            with open(self.__json_file_path, 'r') as fd:
                self.__storage = json.load(fd)
        except FileNotFoundError:
            self.__storage = {}
        self.__dirty = False

    def __save(self):
        with open(self.__json_file_path, 'w') as fd:
            json.dump(self.__storage, fd)
        self.__dirty = False

    def __hold_lock(self):
        self.__lock_fd = open(self.__lock_file_path, 'a')
        fcntl.lockf(self.__lock_fd.fileno(), fcntl.LOCK_EX)

    def __release_lock(self):
        fcntl.lockf(self.__lock_fd.fileno(), fcntl.LOCK_UN)
        self.__lock_fd.close()
        self.__lock_fd = None
