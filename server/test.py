#!flask/bin/python
import unittest
from coverage import coverage

from test import *


if __name__ == '__main__':
    cov = coverage()

    cov.start()
    try:
        unittest.main()
    except:
        pass
    cov.stop()

    print("\n\nCoverage Report:\n")
    cov.save()
    cov.report()

    print("\nHTML version: tmp/coverage/index.html")
    cov.html_report()

    cov.erase()
