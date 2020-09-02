Space managing
==============


Space help
^^^^^^^^^^

.. code-block:: bash

    trood space --help

ls
^^^
Get list of all your spaces

.. code-block:: bash

    trood space ls

Remove space
^^^^^^^^^^^^

.. code-block:: bash

    trood space rm <space_id>

Create space
^^^^^^^^^^^^

.. code-block:: bash

    trood space create <space_name>

Create space from template
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    trood space create <space_name> --template <template_name>

Migrate buisiness objects and load data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
optional argument: -- verbose (-v) shows full error message.

:ref:`fixtures`



.. code-block:: bash

    trood space load_data <space_name> <path_to_file> --verbose --token "Token: d89538ad2f40436fb874e0f0a3ac1e1a"


Publish frontend
^^^^^^^^^^^^^^^^

.. code-block:: bash

    trood space publish <space_name> <path_to_frontend_folder>

