******************************
azure_devops_artifacts_helpers
******************************

.. image:: https://codecov.io/gh/djpugh/azure_devops_artifacts_helpers/branch/master/graph/badge.svg?token=APZ8YDJ0UD
:target: https://codecov.io/gh/djpugh/azure_devops_artifacts_helpers

.. image:: https://app.fossa.com/api/projects/custom%2B20832%2Fgithub.com%2Fdjpugh%2Fazure_devops_artifacts_helpers.svg?type=shield
:target: https://app.fossa.com/projects/custom%2B20832%2Fgithub.com%2Fdjpugh%2Fazure_devops_artifacts_helpers?ref=badge_shield


Bootstrap using Private Azure Devops Artifacts Feeds as an index-url with virtualenv/tox

Install using ``pip install azure_devops_artifacts_helpers``

Then use ``virtualenv <target_dir> --seeder azdo-pip``

To create a virtualenv with the ``artifacts-keyring`` package installed.

This also includes an extension for ``tox``, which will activate automatically (may require configuring
``requires`` in the ``tox`` config)

.. image:: https://codecov.io/gh/djpugh/azure_devops_artifacts_helpers/branch/master/graphs/sunburst.svg?token=APZ8YDJ0UD
:target: https://codecov.io/gh/djpugh/azure_devops_artifacts_helpers

.. image:: https://app.fossa.com/api/projects/custom%2B20832%2Fgithub.com%2Fdjpugh%2Fazure_devops_artifacts_helpers.svg?type=large
:target: https://app.fossa.com/attribution/a496b510-bec3-45b9-902e-4924ecd90cc0

---------------------------

(Built from `package-template <https://github.com/djpugh/package-template>`_ version 1.0.0)