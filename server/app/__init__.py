import os.path

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
configdir = os.path.abspath(os.path.join(basedir, '..', 'config'))
tempdir = os.path.join(basedir, 'tmp')
persistent_storage_dir = os.path.join(configdir, 'persistent_storage')

test_mode = False
doc_mode = False
