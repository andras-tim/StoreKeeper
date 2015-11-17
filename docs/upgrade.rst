.. StoreKeeper documentation

Upgrade
=======

The upgrade process is under construction, but there are the main steps:

1. Update source code with **git** / extract release ``.tar.gz`` from GitHub.
2. Update libs and others with ``./package.sh -p install``.
3. Follow up config changes based on ``config/config.default.yml``.
4. Upgrade database scheme with ``./package.sh upgrade_database``.

.. note::
    Proper, seamless upgrade process will be supported between the stable versions!


Upgrade from v0.2.1 to v0.3.0
-----------------------------

Changed the database migration framework in **v0.3.0**, therefore have to make some changes by hand:

1. Do common upgrade scenario step-by-step **without** upgrading database *(step 4)*
2. Remove ``server/db_repository`` directory
3. Run the following SQL commands:

    .. code-block:: sql

        ALTER TABLE item ALTER COLUMN purchase_price SET DEFAULT 0;

        DROP TABLE migrate_version;
        CREATE TABLE alembic_version (version_num character varying(32) NOT NULL);
        -- ALTER TABLE public.alembic_version OWNER TO sql_user_of_storekeeper;
        INSERT INTO alembic_version VALUES ('305c2b0084f');

4. Now, upgrade database scheme with ``./package.sh upgrade_database``.

.. note::
    Run this commands as StoreKeeper's SQL user or use ``ALTER TABLE`` to set owner of the new table.
