#!/usr/bin/env python3
"""
This file is a workaround for non-fully-clean ReadTheDocs environment

FYI: The docs building will be failed when config structure was changed, because the previous config was present and
this application will not overwrite it.

Please use package.sh scripts for setup.
"""
import os
import shutil
import sys

OBSOLETED_LIST = [
    'config/config.yml',
]


def is_run_on_read_the_docs() -> bool:
    return os.environ.get('READTHEDOCS', None) == 'True'


def cleanup(paths: list):
    for path in paths:
        if os.path.isdir(path):
            print(' * Removing directory {!r}/...'.format(path))
            shutil.rmtree(path)
        elif os.path.isfile(path):
            print(' * Removing file {!r}...'.format(path))
            os.remove(path)


def main():
    if not is_run_on_read_the_docs():
        print(__doc__, file=sys.stderr)
        return 1

    print('Cleanup workspace')
    cleanup(OBSOLETED_LIST)
    print('Done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
