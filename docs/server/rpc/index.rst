.. StoreKeeper documentation

RPC API
=======

**StoreKeeper** uses `HATEOAS`_ RCP API for communicate server and client side each
other. The URLs are prefixed with name of application what you can customize in ``server/config.yml``.

.. _HATEOAS: http://en.wikipedia.org/wiki/HATEOAS

*Example URL:*

    ``http://localhost:8000/<name>/api/<command>``


Contents:

.. toctree::
   :maxdepth: 2

   session
   user
