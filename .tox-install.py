import argparse
import os
import subprocess
import sys

print(sys.version_info, sys.executable)


def run(env_name, extra, input_file):
    _prep()
    _install(_compile(env_name, extra, input_file))

def _prep():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pip-tools'])

def _compile(env_name, extras, input_file):
    output_file = f'requirements-{env_name}.txt'
    args = [sys.executable, '-m', 'piptools', 'compile', input_file, '-o', output_file, '--resolver=backtracking']
    if extras:
        for extra in extras:
            args += ['--extra', extra]
    subprocess.check_call(args)
    return output_file

def _install(requirements_file):
    print(f'Installing from compiled {requirements_file}')
    with open(requirements_file) as f:
        reqs = f.read()
    print(reqs)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
    os.remove(requirements_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name')
    parser.add_argument('--extras', default=None, nargs='*')
    parser.add_argument('--input-file', default='pyproject.toml')
    args = parser.parse_args()
    run(args.env_name, args.extras, args.input_file)