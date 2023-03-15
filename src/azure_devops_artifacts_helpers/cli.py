"""CLI components."""
from pathlib import Path
import subprocess
import sys

import click
from pkg_resources import resource_filename

from azure_devops_artifacts_helpers import __version__


EXT_DIR = Path(resource_filename('azure_devops_artifacts_helpers.wheels', ''))


@click.group('Azure devops artifacts helpers commands')
@click.version_option(version=__version__)
def main():
    """Azure devops artifacts helpers commands."""
    pass


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('pip_args', nargs=-1, type=click.UNPROCESSED)
@click.option('--python', default=sys.executable)
def install(python, pip_args):
    """Azure devops artifacts install artfacts keyring."""
    for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
        # Install it and use the source dir
        args = [python, '-m', 'pip', 'install', str(pkg), '--find-links', f'file://{str(EXT_DIR.as_posix())}']+list(pip_args)
        print(args)
        subprocess.check_call(args)
        return


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('pip_args', nargs=-1, type=click.UNPROCESSED)
@click.option('--python', default=sys.executable)
def uninstall(python, pip_args):
    """Azure devops artifacts uninstall artfacts keyring."""
    # Uninstall it and use the source dir
    for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
        args = [python, '-m', 'pip', 'uninstall', '-y', pkg] + list(pip_args)
        print(args)
        subprocess.check_call(args)
        return


if __name__ == "__main__":
    main()
