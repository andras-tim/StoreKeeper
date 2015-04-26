.. StoreKeeper documentation

Users
=====

API endpoint for manage users.

Data management
---------------

``/api/users``
^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: user_list

``/api/users/<id>``
^^^^^^^^^^^^^^^^^^^
  .. autoflask:: app.server:app
     :endpoints: user
