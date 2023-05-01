import argparse
import os
from pathlib import Path
import subprocess
import sys
from typing import List

print(sys.version_info, sys.executable)


def run(input_file:str) -> None:
    _prep()
    _generate_pipfile(_compile(input_file))

def _prep() -> None:
    if sys.version_info.minor < 11 and sys.version_info.major >= 3:
        print('Installing tomli')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tomli'])

def _compile(input_file: str) -> str:
    if sys.version_info.minor >= 11 and sys.version_info.major >= 3:
        import tomllib as toml
    else:
        import tomli as toml  # type: ignore
    output_file = 'requirements.txt'
    with open(input_file) as f:
        config = toml.loads(f.read())
    dependencies = config['project']['dependencies']
    for extra in config['project']['optional-dependencies']:
        dependencies += config['project']['optional-dependencies'][extra]
    with open(output_file, 'w') as f:
        f.write('\n'.join(dependencies))
    return output_file

def _generate_pipfile(requirements_file: str) -> None:
    if Path('Pipfile').exists():
        os.remove('Pipfile')
    if Path('Pipfile.lock').exists():
        os.remove('Pipfile.lock')
    args = [sys.executable, '-m', 'pipenv', 'lock']
    subprocess.check_call(args)
    os.remove(requirements_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', default='pyproject.toml')
    args = parser.parse_args()
    # Pass un expected args to the install step
    run(args.input_file)
