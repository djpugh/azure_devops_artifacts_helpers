import sys

try:
    import tox
    from tox.venv import cleanup_for_venv, _SKIP_VENV_CREATION, reporter

except (ImportError, ModuleNotFoundError):
    tox = False


if tox:

    @tox.hookimpl
    def tox_testenv_create(venv, action):
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
        args.extend(["--seeder", 'azdo-app-data'])

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
            except KeyboardInterrupt:
                venv.status = "keyboardinterrupt"
                raise
        return True  # Return non-None to indicate plugin has completed


else:
    def tox_venv(venv, action):
        pass
