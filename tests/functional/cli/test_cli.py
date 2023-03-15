from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

TEST_VENV_NAME = '.venv'

if sys.platform.startswith('win'):
    pip_path = Path(TEST_VENV_NAME)/'scripts'/'pip'
    python_path = Path(TEST_VENV_NAME)/'scripts'/'python'
else:
    pip_path = Path(TEST_VENV_NAME)/'bin'/'pip'
    python_path = Path(TEST_VENV_NAME)/'bin'/'python'


class CLITestCase(unittest.TestCase):

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()

    def tearDown(self):
        try:
            self.td.cleanup()
        except PermissionError:
            pass

    def test_install_uninstall(self):
        subprocess.check_call([sys.executable, '-m', 'virtualenv', str(Path(self.td.name)/TEST_VENV_NAME)])
        subprocess.check_call([sys.executable, '-m', 'azure_devops_artifacts_helpers.cli', 'install', '--python', str(Path(self.td.name)/python_path)])
        installed_packages = subprocess.check_output([str(Path(self.td.name)/pip_path), 'freeze']).decode()
        self.assertIn('artifacts-keyring', installed_packages, installed_packages)
        self.assertIn('requests', installed_packages, installed_packages)
        self.assertIn('keyring', installed_packages, installed_packages)
        subprocess.check_call([sys.executable, '-m', 'azure_devops_artifacts_helpers.cli', 'uninstall', '--python', str(Path(self.td.name)/python_path)])
        installed_packages = subprocess.check_output([str(Path(self.td.name)/pip_path), 'freeze']).decode()
        self.assertNotIn('artifacts-keyring', installed_packages, installed_packages)

    def test_install_uninstall_cli(self):
        subprocess.check_call([sys.executable, '-m', 'virtualenv', str(Path(self.td.name)/TEST_VENV_NAME)])
        subprocess.check_call(['azure_devops_artifacts_helpers', 'install','--python', str(Path(self.td.name)/python_path)])
        installed_packages = subprocess.check_output([str(Path(self.td.name)/pip_path), 'freeze']).decode()
        self.assertIn('artifacts-keyring', installed_packages, installed_packages)
        self.assertIn('requests', installed_packages, installed_packages)
        self.assertIn('keyring', installed_packages, installed_packages)
        subprocess.check_call(['azure_devops_artifacts_helpers', 'uninstall', '--python', str(Path(self.td.name)/python_path)])
        installed_packages = subprocess.check_output([str(Path(self.td.name)/pip_path), 'freeze']).decode()
        self.assertNotIn('artifacts-keyring', installed_packages, installed_packages)

    def test_main(self):
        subprocess.check_call([sys.executable, '-m', 'virtualenv', str(Path(self.td.name)/TEST_VENV_NAME)])
        subprocess.check_call([sys.executable, '-m', 'azure_devops_artifacts_helpers', '--python', str(Path(self.td.name)/python_path)])
        installed_packages = subprocess.check_output([str(Path(self.td.name)/pip_path), 'freeze']).decode()
        self.assertIn('artifacts-keyring', installed_packages, installed_packages)
        self.assertIn('requests', installed_packages, installed_packages)
        self.assertIn('keyring', installed_packages, installed_packages)
