.. StoreKeeper documentation

RPC API
=======

.. index:: api

**StoreKeeper** uses `HATEOAS`_ :index:`RCP API` for communicate server and client side each
other. The URLs are prefixed with name of application what you can customize in ``server/config.yml``.


.. _HATEOAS: http://en.wikipedia.org/wiki/HATEOAS

*Example URL:*

    ``http://localhost:8000/<name>/api/<command>``


Endpoints
---------

.. toctree::
   :maxdepth: 2

   sessions
   users
   vendors
   units
   customers
   acquisitions
   acquisition_items
   stocktakings
   stocktaking_items
   items
   barcodes
