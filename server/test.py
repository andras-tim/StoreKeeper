#!./flask/bin/python
import os
import unittest
from coverage import coverage
import sys

import app


def main(args: list) -> bool:
    run_by_ci = "--ci" in args
    suite = unittest.defaultTestLoader.discover(os.path.join(app.basedir, "test"))

    cov = coverage(config_file=os.path.join(app.basedir, ".coveragerc"))
    cov.start()
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    cov.stop()
    cov.save()

    print("\n\nCoverage Report:\n")
    cov.report()

    if not run_by_ci:
        print("\nHTML version: tmp/coverage/index.html")
        cov.html_report()

        cov.erase()

    return len(result.errors) == 0


if __name__ == '__main__':
    if main(sys.argv[1:]):
        sys.exit(0)
    sys.exit(1)
