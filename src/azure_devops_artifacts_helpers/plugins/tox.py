"""Extension for tox to use on environment creation to install artifacts-keyring to virtualenv automatically."""
import sys
from typing import Any

from azure_devops_artifacts_helpers import __name__, __package__
from azure_devops_artifacts_helpers.seed import EXT_DIR

try:
    import tox
except ImportError:  # pragma: no cover
    tox = False

NAME = __name__ or __package__
CLI_PARAM = NAME.replace('_', '-')


def _add_option(parser: Any) -> None:
    """Common method to add cli option."""
    parser.add_argument(f"--disable-{CLI_PARAM}", action="store_true",
                        default=False, help="Disable azure devops artifacts keyring installation")


if tox:  # noqa: C901

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

        @impl  # type: ignore
        def tox_on_install(tox_env: ToxEnv, arguments: Any, section: str, of_type: str) -> None:  # noqa: U100
            """Called before executing an installation command to install artifacts keyring."""
            if tox_env.conf.load(NAME) and not getattr(tox_env.options, f'disable_{NAME}'):
                # To force install from the bundled wheels, we use the following pip flags:
                #    -f EXT_DIR --no-index
                # This makes pip look in the bundled wheel dir, and not use the index
                tox_env.installer._execute_installer(['artifacts-keyring', '-f', EXT_DIR, '--no-index'], 'pre_deps')

        @impl  # type: ignore
        def tox_add_env_config(env_conf: EnvConfigSet, state: State) -> None:  # noqa: U100
            """Add environment config option for ignoring/skipping azure_devops_artifacts_helpers install."""
            env_conf.add_config(keys=NAME,
                                of_type=bool,
                                default=True,
                                desc='Use Azure Devops Artifacts Helpers to seed env')

        @impl  # type: ignore
        def tox_add_option(parser: ToxParser) -> None:
            """Add commandline option."""
            _add_option(parser)

        def tox_testenv_create(venv: Any, action: str) -> None:  # noqa: U100
            """Empty method if tox v4 installed."""

        def tox_addoption(parser: Any) -> None:  # noqa: U100
            """Empty method if tox v4 installed."""

        def tox_configure(config: Any) -> None:  # noqa: U100
            """Empty method if tox v4 installed."""

    else:
        from tox.config import Parser, TestenvConfig
        from tox.venv import cleanup_for_venv, _SKIP_VENV_CREATION, reporter, VirtualEnv

        @tox.hookimpl  # type: ignore
        def tox_testenv_create(venv: VirtualEnv, action: str) -> bool:
            """Hook for creating tox testenv, monkeypatched from tox."""
            if getattr(venv.envconfig, NAME):
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

        @tox.hookimpl  # type: ignore
        def tox_addoption(parser: Parser) -> None:
            """Add the cli option."""
            _add_option(parser)

        @tox.hookimpl  # type: ignore
        def tox_configure(config: TestenvConfig) -> None:
            """Set the config and process the cli option."""
            for env in config.envlist:
                value = not getattr(config.option, f'disable_{NAME}')
                try:
                    value &= config.envconfigs[env]._reader.getbool(NAME, True)
                except AttributeError:
                    value &= True
                setattr(config.envconfigs[env], NAME, value)

        def tox_add_env_config(env_conf: Any, state: Any) -> None:  # noqa: U100
            """Empty method if tox v3 installed."""

        def tox_add_option(parser: Any) -> None:  # noqa: U100
            """Empty method if tox v3 installed."""

else:  # pragma: no cover
    def tox_testenv_create(venv: Any, action: str) -> None:  # noqa: U100
        """Empty method if tox not installed."""

    def tox_on_install(venv: Any, action: str) -> None:  # noqa: U100
        """Empty method if tox not installed."""

    def tox_addoption(parser: Any) -> None:  # noqa: U100
        """Empty method if tox not installed."""

    def tox_configure(config: Any) -> None:  # noqa: U100
        """Empty method if tox not installed."""

    def tox_add_env_config(env_conf: Any, state: Any) -> None:  # noqa: U100
        """Empty method if tox not installed."""

    def tox_add_option(parser: Any) -> None:  # noqa: U100
        """Empty method if tox not installed."""
