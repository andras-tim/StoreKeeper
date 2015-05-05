.. StoreKeeper documentation

Acquisitions
============

API endpoint for manage acquisitions.

Data management
---------------

``/api/acquisitions``
^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: acquisition_list

``/api/acquisitions/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: acquisition

``/api/acquisitions/<id>/items``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: acquisition_item_list

``/api/acquisitions/<id>/items``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: acquisition_item

