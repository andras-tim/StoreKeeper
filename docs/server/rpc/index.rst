.. StoreKeeper documentation

RPC API
=======

.. index:: api

**StoreKeeper** uses `HATEOAS <http://en.wikipedia.org/wiki/HATEOAS>`_ :index:`RCP API` for communicate server and client side each
other. The URLs are prefixed with name of application what you can customize in ``server/config.yml``.

*Example URL:*

    ``http://localhost:8000/<name>/api/<command>``


Endpoints
---------

.. toctree::
    :maxdepth: 3

    acquisitions
    barcodes
    config
    customers
    error
    items
    session
    stocktakings
    units
    users
    vendors
    works
