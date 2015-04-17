![alt tag](https://raw.githubusercontent.com/andras-tim/StoreKeeper/master/client/app/img/logo.png)

[![Build Status](https://travis-ci.org/andras-tim/StoreKeeper.svg?branch=master)](https://travis-ci.org/andras-tim/StoreKeeper)
[![Coverage Status](https://coveralls.io/repos/andras-tim/StoreKeeper/badge.svg?branch=master)](https://coveralls.io/r/andras-tim/StoreKeeper?branch=master)
[![Documentation Status](https://readthedocs.org/projects/storekeeper/badge/?version=latest)](https://readthedocs.org/projects/storekeeper/?badge=latest)
[![License](https://img.shields.io/badge/license-GPL%202.0-blue.svg)](https://github.com/andras-tim/StoreKeeper/blob/master/LICENSE)

StoreKeeper is an open source, multilingual warehouse/store management software

*Project is under development, so pleas go back some weeks later for first release!*


## Features
The following features are only available via API now.

* Manage users, sessions (login, logout), handle permissions
* Manage items and its barcodes, units, vendors
* Can make acquisition, amd stocktaking
* Can crate works and its customers (handle outbound, returned items)


## Prepare & Run
All commands can run with `package.sh` scripts what you want. All of these scripts has `--help` argument for
 available getting some info about the current module.

1. Install all dependencies: `./package.sh install`
2. Check the `./server/config.yml` for database and other settings
3. Prepare database: `./server/database.py --create`
4. Start server: `./package.sh start`

Now, you can open the WebUI: [http://localhost:8000/storekeeper](http://localhost:8000/storekeeper)


## Documentation
You can read more details in documentation. It's available in online and offline format too:

* Run `./package.sh docs` after preparation for offline format
* For online, pre-built docs, please open the [http://storekeeper.readthedocs.org/](http://storekeeper.readthedocs.org/)
