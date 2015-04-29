.. StoreKeeper documentation

Barcodes
========

API endpoint for manage barcodes.

Data management
---------------

``/api/barcodes``
^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: barcode_list

``/api/barcodes/<id>``
^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: barcode

Commands
--------

``/api/barcodes/<id>/print``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: barcode_print

