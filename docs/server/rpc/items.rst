.. StoreKeeper documentation

Items
=====

API endpoint for manage items.

Data management
---------------

``/api/items``
^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: item_list

``/api/items/search``
^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: item_search

``/api/items/<id>``
^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: item

``/api/items/<id>/barcodes``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: item_barcode_list

``/api/items/<id>/barcodes/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: item_barcode

Commands
--------

``/api/items/<id>/barcodes/<id>/print``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: item_barcode_print
