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

``/api/works/<id>/items``
^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work_item_list

``/api/works/<id>/items/<item_id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work_item


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
