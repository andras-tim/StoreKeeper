.. StoreKeeper documentation

Works
=====

Works endpoint of RPC API.

Data management
---------------

``/api/works``
^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: works

``/api/works/<id>``
^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work

Commands
--------

``/api/works/<id>/close-outbound``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work_close_outbound
