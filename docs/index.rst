.. StoreKeeper documentation master file

Welcome to StoreKeeper's documentation!
=======================================

StoreKeeper is an open source, multilingual warehouse/store management software

.. warning::
    *Project is under development, so pleas go back some weeks later for first release!*


Features
--------

The following features are only available via API now.

* Manage users, sessions (login, logout), handle permissions
* Manage items and its barcodes, units, vendors
* Can make acquisition, amd stocktaking
* Can crate works and its customers (handle outbound, returned items)


Demo site
---------
You can test the latest development version on our demo server:
 http://storekeeper-demo.dras.hu/storekeeper

Default username and password: **admin** / **admin**


Languages
---------

StoreKeeper is building in multilingual approach, therefore it can easily translate to a new language.

* You should create a new ``.po`` file in your language, then put to ``client/po/`` directory and create a pull request.
* Or use *Transifex* for online translation: https://www.transifex.com/projects/p/storekeeper/


The Guide
=========

.. toctree::
   :maxdepth: 2

   setup
   client/index
   server/index


Indices and tables
==================

* :ref:`genindex`
