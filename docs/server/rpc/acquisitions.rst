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

