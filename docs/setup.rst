.. StoreKeeper documentation

Setup
=====

Prepare & Run
-------------

.. index:: package.sh, dependencies

All commands can run with ``package.sh`` scripts what you want. All of these scripts has ``--help`` argument for
available getting some info about the current module.

   1. Clone repo, or download & extract a release ``.tar.gz`` file
   2. Install all dependencies: ``./package.sh -p install``
   3. Make default configuration files: ``./package.sh make_defaults``
   4. Check the ``config/config.yml`` for database and other settings
   5. Prepare database: ``./package.sh create_database``
   6. Start server: ``./package.sh start``

Now, you can open the WebUI: http://localhost:8000/storekeeper


Details
-------

Basically, the ``install`` command consists of ``preinstall`` and ``postinstall`` parts.

   * ``preinstall`` checks/prepares system components for ``postinstall`` and ``start``. This command has only one
     dependency, an **DEB** based system (for `apt-get install`).
   * ``postinstall`` checks/prepares external dependencies (e.g. Python, Bower modules).

You can modify installing method with this arguments:

   * ``--global`` makes changes on system instead of virtual environments.
   * ``--production`` installs dependencies for production running only (e.g. did not install unit test framework)
