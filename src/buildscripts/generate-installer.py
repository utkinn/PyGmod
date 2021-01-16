#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path
from pathlib import Path
from itertools import chain
from zipfile import ZipFile


def files(*dir, suffix=''):
    """Returns the list of files in ``dir``, optionally filtering files with suffix ``ext``."""
    return filter(lambda e: e.is_file(), Path(path.join(*dir)).glob('**/*' + suffix))


def generate_common(build_path):
    with ZipFile(build_path / 'common.zip', 'w') as common_zip:
        for file in files('lua'):
            common_zip.write(file, Path('garrysmod') / Path(file).relative_to('lua'))
        for file in files('html'):
            common_zip.write(file, Path('garrysmod', 'pygmod') / file)
        for file in files('python', 'pygmod'):
            common_zip.write(file, Path('garrysmod', 'pygmod') / Path(file).relative_to('python'))
        for file in files('cpp', 'stdlib', 'lib', suffix='.py'):
            common_zip.write(file, Path('garrysmod', 'pygmod', 'stdlib') / Path(file).relative_to('cpp', 'stdlib', 'lib'))


def generate_win32(build_path, args):
    with ZipFile(build_path / 'win32.zip', 'w') as win32_zip:
        bin_build_dir = Path('cpp', 'Debug' if args.debug else 'Release')
        win32_zip.write(bin_build_dir / 'pygmod.dll', 'pygmod.dll')

        python_dll = 'python' + args.python_version 
        python_dll += '_d.dll' if args.debug else '.dll'
        win32_zip.write(Path('cpp', 'cpython-prefix', 'src', 'cpython', 'PCBuild', 'win32', python_dll), python_dll)

        for realm_dll in bin_build_dir.glob('gm*_pygmod_win32.dll'):
            win32_zip.write(realm_dll, Path('garrysmod', 'lua', 'bin') / realm_dll.relative_to(bin_build_dir))

        for file in files('cpp', 'stdlib', 'lib', suffix='.pyd'):
            win32_zip.write(file, Path('garrysmod', 'pygmod') / Path(file).relative_to('cpp'))


def generate_linux32(build_path, args):
    ...


def generate_pyz(build_path):
    with ZipFile(build_path / 'pygmod.pyz', 'w') as pyz:
        for zip_file in ['common', 'win32']:
            pyz.write(build_path / f'{zip_file}.zip', f'{zip_file}.zip')
        pyz.write(Path('python', 'installer', '__main__.py'), '__main__.py')


def main():
    argp = ArgumentParser(description='Builds `pygmod.pyz` to `installer-build`.')
    argp.add_argument('-d', '--debug', action='store_true', help='look for files produced by debug build')
    argp.add_argument('python_version', help='embedded Python version without a dot (i. e. 38 for Python 3.8)')
    args = argp.parse_args()

    # installer-build/tree/{common,linux32,win32} is where the files
    # for respective archives go
    build_path = Path('installer-build')
    build_path.mkdir(exist_ok=True)
    generate_common(build_path)
    generate_win32(build_path, args)
    generate_pyz(build_path)


if __name__ == "__main__":
    main()
