Development
===========

Getting started
---------------


``azure_devops_artifacts_helpers`` is a volunteer maintained open source project and we welcome contributions of all forms. The sections
below will help you get started with development, testing, and documentation. We’re pleased that you are interested in
working on ``azure_devops_artifacts_helpers``. This document is meant to get you setup to work on ``azure_devops_artifacts_helpers`` and to act as a guide and reference
to the development setup. If you face any issues during this process, please
`open an issue <https://github.com/djpugh/azure_devops_artifacts_helpers/issues/new?title=Trouble+with+development+environment>`_ about it on
the issue tracker.

Setup
~~~~~

``azure_devops_artifacts_helpers`` is an extension to :pypi:`virtualenv`, written in Python. To work on it, you'll need:

- **Source code**: available on `GitHub <https://github.com/djpugh/azure_devops_artifacts_helpers>`_. You can use ``git`` to clone the
    repository:

  .. code-block:: console

      git clone https://github.com/djpugh/azure_devops_artifacts_helpers
      cd azure_devops_artifacts_helpers

- **Python interpreter**: We recommend using ``CPython``. You can use
  `this guide <https://realpython.com/installing-python/>`_ to set it up.

- :pypi:`tox`: to automatically get the projects development dependencies and run the test suite.



Running from source tree
~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to do this is to generate the development tox environment, and then invoke ``azure_devops_artifacts_helpers`` from under the
``.venv`` folder

.. code-block:: console

    tox -e develop
    .venv/Scripts/virtualenv  # on Windows


Populating wheels
~~~~~~~~~~~~~~~~~

Due to challenges with :pypi:`pip` ``download``, the full set of wheels is popualated at build time based on the provided ``embed_requirements.txt``.
When developing locally (and e.g. for testing locally), it's necessary to populate the wheels for that platform. The easiest way to do this is using
``tox``

.. code-block:: console

    tox -e populate


Running tests
~~~~~~~~~~~~~

``azure_devops_artifacts_helpers`` tests are written using the :pypi:`pytest` test framework. :pypi:`tox` is used to automate the setup
and execution of ``azure_devops_artifacts_helpers`` tests. This requires populating the wheels (see above).

To run tests locally execute:

.. code-block:: console

    tox -e test-v3,test-v4

This will run the test suite for the same Python version as under which ``tox`` is installed.



Running linters
~~~~~~~~~~~~~~~

``azure_devops_artifacts_helpers`` uses :pypi:`flake8` and extensions for managing linting of the codebase. ``flake8`` performs various checks on all
files in ``azure_devops_artifacts_helpers`` and uses tools that help follow a consistent code style within the codebase. To use linters locally,
run:

.. code-block:: console

    tox -e lint

.. note::

    Avoid using ``# noqa`` comments to suppress linter warnings - wherever possible, warnings should be fixed instead.
    ``# noqa`` comments are reserved for rare cases where the recommended style causes severe readability problems.

Building documentation
~~~~~~~~~~~~~~~~~~~~~~

``azure_devops_artifacts_helpers`` documentation is built using :pypi:`Sphinx`. The documentation is written in reStructuredText. To build it
locally, run:

.. code-block:: console

    tox -e docs

The built documentation can be found in the ``docs/html`` folder and may be viewed by opening ``index.html`` within
that folder.

Release
~~~~~~~

We release after new :pypi:`virtualenv` and :pypi:`artifacts-keyring` releases to confirm that our extensions are still working.

Contributing
-------------

Submitting pull requests
~~~~~~~~~~~~~~~~~~~~~~~~

Submit pull requests against the ``main`` branch, providing a good description of what you're doing and why. You must
have legal permission to distribute any code you contribute to ``azure_devops_artifacts_helpers`` and it must be available under the MIT
License. Provide tests that cover your changes and run the tests locally first. ``azure_devops_artifacts_helpers``
supports multiple Python (and tox) versions. Any pull request must consider and work on all these platforms.

Pull Requests should be small to facilitate review, avoid including "cosmetic" changes to code that is unrelated to your change, as these make reviewing the
PR more difficult. Examples include re-flowing text in comments or documentation, or addition or removal of blank lines
or whitespace within lines. Such changes can be made separately, as a "formatting cleanup" PR, if needed.

Automated testing
~~~~~~~~~~~~~~~~~

All pull requests and merges to ``main`` branch are tested using Github actions (configured by ``.github/workflows/pipeline.yml`` file. You can find the status and results to the CI runs for your
PR on GitHub's Web UI for the pull request.
