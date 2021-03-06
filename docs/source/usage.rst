Using azure_devops_artifacts_helpers
====================================


:pypi:`azure_devops_artifacts_helpers` is an extension to :pypi:`virtualenv`. Once installed, you should see ``azdo-pip`` 
in the ``--seeders`` options when running ``virtualenv --help``.

To create a virtualenv with |artifacts_keyring_version| installed use::

    $ virtualenv <venv-name> --seeders=azdo-pip

There is also a tox plugin that can be included using the ``tox`` ``requires`` argument in ``tox.ini``

.. code-block:: ini

    [tox]
    envlist = ...
    requires =
        azure_devops_artifacts_helpers

    ...

Which will enforce installing it and therefore enable ``artifacts-keyring`` and its dependencies to be installed in any new tox env.
