#!../flask/bin/python
"""
Fill up database with huge amount of test data
"""
import os.path
import sys

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(basedir)

from app.server import db


def main():
    pass


if __name__ == "__main__":
    sys.exit(main())

