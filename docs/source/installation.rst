Installation
============


:pypi:`azure_devops_artifacts_helpers` is an extension to :pypi:`virtualenv` that preconfigures with Azure DevOps
Artifacts authentication using ``artifacts-keyring``. If you already have :pypi:`virtualenv` installed in an environment,
then use the installer of your choice to install this into the same environment.

e.g. pip
--------

You can install it using pip (please see `the caveats <https://virtualenv.pypa.io/en/latest/installation.html#via-pip>`_ 
about affecting global python installs, and make sure this is installed in the same environment as :pypi:`virtualenv`)

.. code-block:: console

    python -m pip install --user azure_devops_artifacts_helpers
    python -m virtualenv --help  # should see azdo-pip in the --seeders options


.. warning::
    ``azure_devops_artifacts_helpers`` currently only works on windows due to issues downloading ``dotnetcore2``
