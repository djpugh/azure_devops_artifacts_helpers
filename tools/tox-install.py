import argparse
import os
import subprocess
import sys
from typing import List

print(sys.version_info, sys.executable)


def run(deps: List[str], env_name: str, input_file:str, opts: List[str]) -> None:
    _prep()
    _install(_compile(deps, env_name, input_file), opts)

def _prep() -> None:
    if sys.version_info.minor < 11 and sys.version_info.major >= 3:
        print('Installing tomli')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tomli'])

def _compile(deps: List[str], env_name: str, input_file: str) -> str:

    if sys.version_info.minor >= 11 and sys.version_info.major >= 3:
        import tomllib as toml
    else:
        import tomli as toml  # type: ignore
    output_file = f'requirements-{env_name}.txt'
    with open(input_file) as f:
        config = toml.loads(f.read())
    packages = []
    for dependency in deps:
        if dependency.startswith('.'):
            # extra
            extra = dependency.split('[', 1)[-1].split(']', 1)[0]
            packages += config['project']['optional-dependencies'][extra]
            print(f'Adding dependencies for {extra}')
        else:
            packages.append(dependency)
    with open(output_file, 'w') as f:
        f.write('\n'.join(packages))
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
    parser.add_argument('deps', default=None, nargs='*')
    parser.add_argument('--input-file', default='pyproject.toml')
    args, opts = parser.parse_known_args()
    print (args, opts)
    # Pass un expected args to the install step
    run(args.deps, args.env_name, args.input_file, opts)
