"""Extension for tox to use on environment creation to install artifacts-keyring to virtualenv automatically."""
import sys
from typing import Any

from packaging.requirements import Requirement

try:
    import tox
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    tox = False

PARAM = 'azure-devops-artifacts-helpers'


def _add_option(parser):
    """Common method to add cli option."""
    parser.add_argument(f"--disable-{PARAM}", action="store_true",
                        default=False, help="Disable azure devops artifacts keyring installation")


if tox:

    try:
        tox_v4 = tox.version.version_tuple[0] > 3
    except AttributeError:
        tox_v4 = False  # Version 3

    if tox_v4:
        from tox.plugin import impl
        from tox.tox_env.api import ToxEnv
        from tox.config.cli.parser import ToxParser
        from tox.config.sets import EnvConfigSet
        from tox.session.state import State

        @impl
        def tox_on_install(tox_env: ToxEnv, arguments: Any, section: str, of_type: str) -> None:  # noqa: U100
            """Called before executing an installation command to install artifacts keyring."""
            if tox_env.conf.load(PARAM.replace("-", "_")) and not getattr(tox_env.options, f'disable_{PARAM.replace("-", "_")}'):
                tox_env.installer.install([Requirement('artifacts-keyring')], tox_env.__class__.__name__, 'pre_deps')

        @impl
        def tox_add_env_config(env_conf: EnvConfigSet, state: State):
            """Add environment config option for ignoring/skipping azure_devops_artifacts_helpers install."""
            env_conf.add_config(keys=PARAM.replace("-", "_"),
                                of_type=bool,
                                default=True,
                                desc='Use Azure Devops Artifacts Helpers to seed env')

        @impl
        def tox_add_option(parser: ToxParser) -> None:
            """Add commandline option."""
            _add_option(parser)

    else:
        from tox.venv import cleanup_for_venv, _SKIP_VENV_CREATION, reporter

        @tox.hookimpl
        def tox_testenv_create(venv, action):
            """Hook for creating tox testenv, monkeypatched from tox."""
            if getattr(venv.envconfig, PARAM.replace('-', '_')):
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

        @tox.hookimpl
        def tox_addoption(parser):
            """Add the cli option."""
            _add_option(parser)

        @tox.hookimpl
        def tox_configure(config):
            """Set the config and process the cli option."""
            value = not getattr(config.option, f'disable_{PARAM.replace("-", "_")}')
            for env in config.envlist:
                try:
                    value &= config.envconfigs[env]._reader.getargv(PARAM.replace('-', '_'), True)
                except AttributeError:
                    value &= True
                setattr(config.envconfigs[env], PARAM.replace('-', '_'), value)
