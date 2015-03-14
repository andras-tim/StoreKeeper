.. StoreKeeper documentation

Setup
=====

Prepare & Run
-------------

.. index:: package.sh, dependencies

All commands can run with ``package.sh`` scripts what you want. All of these scripts has ``--help`` argument for
available getting some info about the current module.

   1. Install all dependencies: ``./package.sh install``
   2. Check the ``./server/config.yml`` for database and other settings
   3. Prepare database: ``./server/database.py --create``
   4. Start server: ``./package.sh start``

Now, you can manage server via RPC API on http://localhost:8000/storekeeper


Details
-------

Basically, the ``install`` command consists of ``preinstall`` and ``postinstall`` parts.

   * ``preinstall`` checks/prepares system components for ``postinstall`` and ``start``. This command has only one
     dependency, an **DEB** based system (for `apt-get install`).
   * ``postinstall`` checks/prepares external dependencies (e.g. Python, Bower modules).

You can modify installing method with this arguments:

   * ``--global`` makes changes on system instead of virtual environments.
   * ``--production`` installs dependencies for production running only (e.g. did not install unit test framework)
