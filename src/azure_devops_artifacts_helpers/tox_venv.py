"""Extension for tox to use on environment creation to install artifacts-keyring to virtualenv automatically."""
import sys
from typing import Any

from packaging.requirements import Requirement

from azure_devops_artifacts_helpers.seed import EXT_DIR

try:
    import tox
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    tox = False

if tox:

    try:
        tox_v4 = tox.version.version_tuple[0] > 3
    except AttributeError:
        tox_v4 = False  # Version 3

    if tox_v4:
        from tox.plugin import impl
        from tox.tox_env.api import ToxEnv

        def tox_testenv_create(venv, action):
            """Empty method if tox v4 installed."""

        @impl
        def tox_on_install(tox_env: ToxEnv, arguments: Any, section: str, of_type: str) -> None:  # noqa: U100
            """Called before executing an installation command to install artifacts keyring."""
            # To force install from the bundled wheels, we use the following pip flags:
            #    -f EXT_DIR --no-index
            # This makes pip look in the bundled wheel dir, and not use the index
            tox_env.installer._execute_installer(['artifacts-keyring', '-f', EXT_DIR, '--no-index'], 'pre_deps')


    else:
        from tox.venv import cleanup_for_venv, _SKIP_VENV_CREATION, reporter

        @tox.hookimpl
        def tox_testenv_create(venv, action):
            """Hook for creating tox testenv, monkeypatched from tox."""
            config_interpreter = venv.getsupportedinterpreter()
            args = [sys.executable, "-m", "virtualenv"]
            if venv.envconfig.sitepackages:
                args.append("--system-site-packages")
            if venv.envconfig.alwayscopy:
                args.append("--always-copy")
            if not venv.envconfig.download:
                args.append("--no-download")
            # add interpreter explicitly, to prevent using default (virtualenv.ini)
            args.extend(["--python", str(config_interpreter)])
            # Add seeder explicitly
            args.extend(["--seeder", 'azdo-pip'])

            cleanup_for_venv(venv)

            base_path = venv.path.dirpath()
            base_path.ensure(dir=1)
            args.append(venv.path.basename)
            if not _SKIP_VENV_CREATION:
                try:
                    venv._pcall(
                        args,
                        venv=False,
                        action=action,
                        cwd=base_path,
                        redirect=reporter.verbosity() < reporter.Verbosity.DEBUG,
                    )
                except KeyboardInterrupt:  # pragma: no cover
                    venv.status = "keyboardinterrupt"
                    raise
            # Return non-None to indicate plugin has completed
            return True

        def tox_on_install(venv, action):
            """Empty method if tox v3 installed."""

else:  # pragma: no cover
    def tox_testenv_create(venv, action):
        """Empty method if tox not installed."""

    def tox_on_install(venv, action):
        """Empty method if tox not installed."""
