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

