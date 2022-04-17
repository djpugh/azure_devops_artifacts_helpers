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
    pass


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('pip_args', nargs=-1, type=click.UNPROCESSED)
def install(pip_args):
    for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
        # Install it and use the source dir
        args = [sys.executable, '-m', 'pip', 'install', str(pkg), '--find-links', f'file://{str(EXT_DIR.as_posix())}']+list(pip_args)
        print(args)
        subprocess.check_call(args)
        return


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('pip_args', nargs=-1, type=click.UNPROCESSED)
def uninstall(pip_args):
    # Uninstall it and use the source dir
    for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
        args = [sys.executable, '-m', 'pip', 'uninstall', pkg] +list(pip_args)
        print(args)
        subprocess.check_call(args)
        return


if __name__ == "__main__":
    install()
