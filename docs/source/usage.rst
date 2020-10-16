Using azure_devops_artifacts_helpers
====================================


:pypi:`azure_devops_artifacts_helpers` is an extension to :pypi:`virtualenv`. Once installed, you should see ``azdo-pip`` 
in the ``--seeders`` options when running ``virtualenv --help``.

There is also a tox plugin that can be included using the ``tox`` ``requires`` argument in ``tox.ini``

.. code-block:: ini

    [tox]
    envlist = ...
    requires =
        azure_devops_artifacts_helpers

    ...

Which will enforce installing it and therefore enable ``artifacts-keyring`` and its dependencies to be installed in any new tox env.

.. warning::
    ``azure_devops_artifacts_helpers`` currently only works on windows due to issues downloading ``dotnetcore2``