.. StoreKeeper documentation

Customers
=========

API endpoint for manage customers.

Data management
---------------

``/api/customers``
^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: customer_list

``/api/customers/<id>``
^^^^^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: customer

