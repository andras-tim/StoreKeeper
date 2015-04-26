.. StoreKeeper documentation

Acquisition Items
=================

API endpoint for manage items of acquisition.

Data management
---------------

``/api/acquisition-items``
^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: acquisition_item_list

``/api/acquisition-items/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: acquisition_item

