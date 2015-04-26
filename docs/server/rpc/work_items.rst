.. StoreKeeper documentation

Work Items
==========

API endpoint for manage items of work.

Data management
---------------

``/api/work-items``
^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work_item_list

``/api/work-items/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: work_item

