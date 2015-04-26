.. StoreKeeper documentation

Works
=====

API endpoint for manage works.

Data management
---------------

``/api/works``
^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work_list

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

``/api/works/<id>/close-returned``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work_close_returned
