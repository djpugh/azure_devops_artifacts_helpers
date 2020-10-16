************************
azure_devops_artifacts_helpers
************************

Bootstrap using Private Azure Devops Artifacts Feeds as an index-url with virtualenv/tox

Install using ``pip install azure_devops_artifacts_helpers``

Then use ``virtualenv <target_dir> --seed <azdo-app-data|azdo-pip>``

To create a virtualenv with the ``artifacts-keyring`` package installed.

This also includes an extension for ``tox``, which will activate automatically (may require configuring
``requires`` in the ``tox`` config)

---------------------------

(Built from `package-template <https://github.com/djpugh/package-template>`_ version 1.0.0)