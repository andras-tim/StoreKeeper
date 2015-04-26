.. StoreKeeper documentation

Stocktaking Items
=================

API endpoint for manage items of stocktaking.

Data management
---------------

``/api/stocktaking-items``
^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: stocktaking_item_list

``/api/stocktaking-items/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: stocktaking_item

