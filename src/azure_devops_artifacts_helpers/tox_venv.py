"""Extension for tox to use on environment creation to install artifacts-keyring to virtualenv automatically."""
import sys

try:
    import tox
    from tox.venv import cleanup_for_venv, _SKIP_VENV_CREATION, reporter

except (ImportError, ModuleNotFoundError):  # pragma: no cover
    tox = False


if tox:

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


else:  # pragma: no cover
    def tox_venv(venv, action):
        """Empty method if tox not installed."""
