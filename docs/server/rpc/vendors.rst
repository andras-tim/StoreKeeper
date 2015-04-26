.. StoreKeeper documentation

Vendors
=======

API endpoint for manage vendors.

Data management
---------------

``/api/vendors``
^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: vendor_list

``/api/vendors/<id>``
^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: vendor

