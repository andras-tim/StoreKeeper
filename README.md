# StoreKeeper
[![Code Health](https://landscape.io/github/andras-tim/StoreKeeper/master/landscape.svg?style=flat)](https://landscape.io/github/andras-tim/StoreKeeper/master)


## About
StoreKeeper is an open source, multilingual warehouse/store management software


## Features
*Currently, this is empty ;)*


## Prepare & Run
All commands can run with `package.sh` scripts what you want. All of these scripts has `--help` argument for
 available getting some info about the current module.

1. Install all dependencies: `./package.sh install`
2. Check the `./server/config.yml` for database and other settings
3. Prepare database: `./server/db_create.py`
4. Run application: `./package.sh start`
5. Open [http://localhost:8000](http://localhost:8000) in a browser


### Details ###
Basically, the `install` command consists of `preinstall` and `postinstall` parts.
* `preinstall` checks/prepares system components for `postinstall` and `start`. This command has only one dependency, an **DEB** based system (for `apt-get install`).
* `postinstall` checks/prepares external dependencies (e.g. Python, Bower modules).

You can modify installing method with this arguments:
* `--global` makes changes on system instead of virtual environments.
* `--production` installs dependencies for production running only (e.g. did not install unit test framework)
