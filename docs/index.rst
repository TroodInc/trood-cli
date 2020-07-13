Trood CLI
=========


Install
~~~~~~~
Install trood-cli.

::

    pip install trood-cli

Info
~~~~

::

    $ trood info

Help
~~~~

::

    $ trood --help

Login
~~~~~
Login in system using your pasport from tcp.trood.com

::

    $ trood login

Logout
~~~~~~

::

    $ trood logout


Space managing
==============

Space help
~~~~~~~~~~

::

    $ trood space --help

ls
~~~
Get list of all your spaces

::

    $ trood space ls

Remove space
~~~~~~~~~~~~

::

    $ trood space rm <space_id>

Create space
~~~~~~~~~~~~

::

    $ trood space create <space_name>

Create space from template
~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    $ trood space create <space_name> --template <template_name>

Publish frontend
~~~~~~~~~~~~~~~~
::

    $ trood space publish <space_name> <path_to_frontend_folder>


.. toctree::
    :maxdepth: 2
    :glob:

