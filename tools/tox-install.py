import argparse
import os
import subprocess
import sys
from typing import List

print(sys.version_info, sys.executable)


def run(env_name: str, extra: List[str], input_file:str, opts: List[str]) -> None:
    if opts:
        subprocess.check_call([sys.executable, '-I', '-m', 'pip', 'install']+opts)
    else:
        _prep()
        _install(_compile(env_name, extra, input_file), opts)

def _prep() -> None:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pip-tools'])

def _compile(env_name: str, extras: List[str], input_file: str) -> str:
    output_file = f'requirements-{env_name}.txt'
    args = [sys.executable, '-m', 'piptools', 'compile', input_file, '-o', output_file, '--resolver=backtracking']
    if extras:
        for extra in extras:
            args += ['--extra', extra]
    subprocess.check_call(args)
    return output_file

def _install(requirements_file: str, opts: List[str]) -> None:
    print(f'Installing from compiled {requirements_file}')
    with open(requirements_file) as f:
        reqs = f.read()
    print(reqs)
    args = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
    if opts:
        args += opts
    subprocess.check_call(args)
    os.remove(requirements_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name')
    parser.add_argument('--extras', default=None, nargs='*')
    parser.add_argument('--input-file', default='pyproject.toml')
    args, opts = parser.parse_known_args()
    print (args, opts)
    # Pass un expected args to the install step
    run(args.env_name, args.extras, args.input_file, opts)
