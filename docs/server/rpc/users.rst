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


Config management
-----------------

``/api/users/<id>/config``
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoflask:: app.server:app
    :endpoints: user_config_list

``/api/users/<id>/config/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoflask:: app.server:app
    :endpoints: user_config
