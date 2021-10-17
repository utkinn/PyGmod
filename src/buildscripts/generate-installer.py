#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path
import sys
from pathlib import Path
from itertools import chain
from zipfile import ZipFile


def files(*dir, suffix=''):
    """Returns the list of files in ``dir``, optionally filtering files with suffix ``ext``."""
    return filter(lambda e: e.is_file(), Path(path.join(*dir)).glob('**/*' + suffix))


def generate_common(build_path, args):
    with ZipFile(build_path / 'common.zip', 'w') as common_zip:
        pygmod_path = Path('garrysmod', 'pygmod')

        for file in files('lua'):
            common_zip.write(file, Path('garrysmod') / file.relative_to('lua'))
        for file in files('html'):
            common_zip.write(file, pygmod_path / file)
        for file in files('python', 'pygmod'):
            common_zip.write(file, pygmod_path / file.relative_to('python'))
        if sys.platform.startswith('win32'):
            for file in files('cpp', 'stdlib', 'lib', suffix='.py'):
                common_zip.write(file, pygmod_path / 'stdlib' / file.relative_to('cpp', 'stdlib', 'lib'))
        elif sys.platform.startswith('linux'):
            for file in files('cpp', 'cpython-out', 'lib', 'python' + args.python_version, suffix='.py'):
                common_zip.write(file, pygmod_path / 'stdlib' / file.relative_to('cpp', 'cpython-out', 'lib', 'python' + args.python_version))


def generate_win32(build_path, args):
    with ZipFile(build_path / f'win{args.bits}.zip', 'w') as win_zip:
        bin_build_dir = Path('cpp', 'Debug' if args.debug else 'Release')
        win_zip.write(bin_build_dir / 'pygmod.dll', Path('garrysmod', 'lua', 'bin', f'gmsv_pygmod_win{args.bits}.dll'))
        win_zip.write(bin_build_dir / 'pygmod.dll', Path('garrysmod', 'lua', 'bin', f'gmcl_pygmod_win{args.bits}.dll'))

        python_dll = 'python' + args.python_version.replace('.', '')
        python_dll += '_d.dll' if args.debug else '.dll'
        pcbuild_dir = 'win32' if args.bits == 32 else 'amd64'
        win_zip.write(Path('cpp', 'cpython-prefix', 'src', 'cpython', 'PCBuild', pcbuild_dir, python_dll), python_dll)

        for file in files('cpp', 'stdlib', 'lib', suffix='.pyd'):
            win_zip.write(file, Path('garrysmod', 'pygmod') / file.relative_to('cpp'))


def generate_linux(build_path, args):
    with ZipFile(build_path / f'linux{args.bits}.zip', 'w') as linux_zip:
        build_path = Path('cpp')
        libpython_filename = 'libpython' + args.python_version + '.so.1.0'
        linux_zip.write(build_path / Path('cpython-out', 'lib', libpython_filename), Path('bin') / libpython_filename)

        linux_zip.write(build_path / Path('libpygmod.so'), Path('garrysmod', 'lua', 'bin', 'gmsv_pygmod_linux64.dll'))
        linux_zip.write(build_path / Path('libpygmod.so'), Path('garrysmod', 'lua', 'bin', 'gmcl_pygmod_linux64.dll'))

        stdlib_path = build_path / Path('cpython-out', 'lib', 'python' + args.python_version, 'lib-dynload')
        for file in files(stdlib_path):
            linux_zip.write(file, Path('garrysmod', 'pygmod', 'stdlib', 'lib-dynload') / file.relative_to(stdlib_path))


def generate_pyz(build_path, args):
    with ZipFile(args.out, 'w') as pyz:
        pyz.write(build_path / 'common.zip', 'common.zip')
        if sys.platform.startswith('win32'):
            pyz.write(build_path / f'win{args.bits}.zip', f'win{args.bits}.zip')
        elif sys.platform.startswith('linux'):
            pyz.write(build_path / f'linux{args.bits}.zip', f'linux{args.bits}.zip')
        pyz.write(Path('python', 'installer', '__main__.py'), '__main__.py')


def main():
    argp = ArgumentParser(description='Builds the PyGmod installer.')
    argp.add_argument('-d', '--debug', action='store_true', help='look for files produced by debug build')
    argp.add_argument('-b', '--bits', type=int, choices=[32, 64], default=32, help='build bitness')
    argp.add_argument('python_version', help='embedded Python version (i. e. 3.8)')
    argp.add_argument('out', help='installer path')
    args = argp.parse_args()

    # installer-build/tree/{common,linux32,win32} is where the files
    # for respective archives go
    build_path = Path('installer-build')
    build_path.mkdir(exist_ok=True)
    generate_common(build_path, args)
    if sys.platform.startswith('win32'):
        generate_win32(build_path, args)
    elif sys.platform.startswith('linux'):
        generate_linux(build_path, args)
    generate_pyz(build_path, args)


if __name__ == "__main__":
    main()
