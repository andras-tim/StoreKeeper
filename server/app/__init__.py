import os.path

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
configdir = os.path.abspath(os.path.join(basedir, '..', 'config'))
tempdir = os.path.join(basedir, 'tmp')
test_mode = False
doc_mode = False
