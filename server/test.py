#!./flask/bin/python
import os
import unittest
from coverage import coverage

import app


if __name__ == '__main__':
    cov = coverage()
    suite = unittest.defaultTestLoader.discover(os.path.join(app.basedir, "test"))

    cov.start()
    try:
        unittest.TextTestRunner(verbosity=1).run(suite)
    except:
        pass
    cov.stop()

    print("\n\nCoverage Report:\n")
    cov.save()
    cov.report()

    print("\nHTML version: tmp/coverage/index.html")
    cov.html_report()

    cov.erase()
