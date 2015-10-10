|Logo|

|Build| |Docs| |DependencyStatus| |CodeQuality| |CoverageServer| |CoverageClient| |License|

StoreKeeper is an open source, multilingual warehouse/store management software

*Project is under development!*


Features
--------

The following features are available:

* User login, logout
* Manage items and its barcodes, units, vendors
* Add/remove items in store
* Able to use barcode reader for collecting items
* Can use barcode printer to create labels

The following features are only available via API now:

* Manage users, handle permissions
* Can make acquisition and stocktaking
* Can crate works and its customers (handle outbound, returned items)


Prepare & Run
-------------

All commands can run with ``package.sh`` scripts what you want. All of these scripts has ``--help`` argument for
available getting some info about the current module.

1. Clone repo, or download & extract a release ``.tar.gz`` file
2. Install all dependencies: ``./package.sh -p install``
3. Make default configuration files: ``./package.sh make_defaults``
4. Check the ``config/config.yml`` for database and other settings
5. Prepare database: ``./package.sh create_database``
6. Start server: ``./package.sh start``

Now, you can open the WebUI: http://localhost:8000/storekeeper


Demo site
---------

You can test the latest development version on our demo server:
 http://storekeeper-demo.dras.hu/storekeeper

Default username and password: **admin** / **admin**


Documentation
-------------

You can read more details in documentation. It's available in online and offline format too:

* Run ``./package.sh docs`` after preparation for offline format
* For online, pre-built docs, please open the http://storekeeper.readthedocs.org


Languages
---------

StoreKeeper is building in multilingual approach, therefore it can easily translate to a new language.

* You should create a new ``.po`` file in your language, then put to ``client/po/`` directory and create a pull request.
* Or use *Transifex* for online translation: https://www.transifex.com/projects/p/storekeeper/

**Top translations:**
 |TranslationState|



.. |Logo| image:: https://raw.githubusercontent.com/andras-tim/StoreKeeper/master/config/img/logo.default.png

.. |Build| image:: https://travis-ci.org/andras-tim/StoreKeeper.svg?branch=master
   :target: https://travis-ci.org/andras-tim/StoreKeeper
   :alt: Build Status
.. |DependencyStatus| image:: https://gemnasium.com/andras-tim/StoreKeeper.svg
   :target: https://gemnasium.com/andras-tim/StoreKeeper
   :alt: Dependency Status
.. |Docs| image:: https://readthedocs.org/projects/storekeeper/badge/?version=latest
   :target: http://storekeeper.readthedocs.org/latest/
   :alt: Documentation Status
.. |License| image:: https://img.shields.io/badge/license-GPL%202.0-blue.svg
   :target: https://github.com/andras-tim/StoreKeeper/blob/master/LICENSE
   :alt: License

.. |CodeQuality| image:: https://www.codacy.com/project/badge/6c9fb93d1b1d4333a8146e8aeb55b11f
   :target: https://www.codacy.com/app/andras-tim/StoreKeeper
   :alt: Code Quality
.. |CodeClimate| image:: https://codeclimate.com/github/andras-tim/StoreKeeper/badges/gpa.svg
   :target: https://codeclimate.com/github/andras-tim/StoreKeeper/coverage
   :alt: Code Climate
.. |CoverageServer| image:: https://coveralls.io/repos/andras-tim/StoreKeeper/badge.svg?branch=master&service=github
   :target: https://coveralls.io/r/andras-tim/StoreKeeper?branch=master&service=github
   :alt: Server Test Coverage
.. |CoverageClient| image:: https://codeclimate.com/github/andras-tim/StoreKeeper/badges/coverage.svg
   :target: https://codeclimate.com/github/andras-tim/StoreKeeper/coverage
   :alt: Client Test Coverage
.. |IssueStats| image:: https://img.shields.io/github/issues/andras-tim/StoreKeeper.svg
   :target: http://issuestats.com/github/andras-tim/StoreKeeper
   :alt: Issue Stats

.. |TranslationState| image:: https://www.transifex.com/projects/p/storekeeper/resource/client/chart/image_png
   :target: https://www.transifex.com/projects/p/storekeeper/
   :alt: See more information on Transifex.com
