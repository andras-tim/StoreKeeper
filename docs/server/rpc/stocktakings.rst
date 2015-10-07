.. StoreKeeper documentation

Stocktakings
============

API endpoint for manage stocktaking results.

Data management
---------------

``/api/stocktakings``
^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: stocktaking_list

``/api/stocktakings/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: stocktaking

``/api/stocktakings/<id>/items``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: stocktaking_item_list

``/api/stocktakings/<id>/items/<item_id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: stocktaking_item


Commands
--------

``/api/stocktakings/<id>/close``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: stocktaking_close
