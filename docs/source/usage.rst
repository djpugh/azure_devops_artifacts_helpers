Using azure_devops_artifacts_helpers
====================================


:pypi:`azure_devops_artifacts_helpers` is an extension to :pypi:`virtualenv`. Once installed, you should see ``azdo-pip``
in the ``--seeders`` options when running ``virtualenv --help``.

To create a virtualenv with |artifacts_keyring_version| installed use::

    $ virtualenv <venv-name> --seeder=azdo-pip

There is also a tox plugin that can be included using the ``tox`` ``requires`` argument in ``tox.ini``

.. code-block:: ini

    [tox]
    envlist = ...
    requires =
        azure_devops_artifacts_helpers

    ...

Which will enforce installing it and therefore enable ``artifacts-keyring`` and its dependencies to be installed in any new tox env.
(for tox v3 this uses the ``tox_testenv_create`` hook, for v4, this hook no longer exists, but instead the more convenient ``tox_on_install`` hook is used)

For tox v4 and later, the ``azure_devops_artifacts_helpers`` config option can be set to ``True`` or ``False`` (defaults to ``True``),
to select whether or not it is used in that environment.