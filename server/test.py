#!./flask/bin/python
import os
import unittest
import sys

import app


def main() -> bool:
    suite = unittest.defaultTestLoader.discover(os.path.join(app.basedir, "test"))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return len(result.errors) == 0


if __name__ == '__main__':
    if main():
        sys.exit(0)
    sys.exit(1)
