#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from zipfile import ZipFile
import os
import sys
import logging

from file_copier import Copier

logger = logging.getLogger(__name__)


def main():
    argp = ArgumentParser(description='Builds the PyGmod installer.')
    argp.add_argument('-d', '--debug', action='store_true',
                      help='look for files produced by debug build')
    argp.add_argument('-b', '--bits', type=int,
                      choices=[32, 64], default=32, help='build bitness')
    argp.add_argument('python_version',
                      help='embedded Python version (i. e. 3.8)')
    argp.add_argument('build_dir', type=Path, help='CMake build directory')
    argp.add_argument('out', help='build installer file path')
    args = argp.parse_args()

    installer_path = args.build_dir / 'installer'
    src_path = Path(__file__).parent.parent

    with open(src_path / 'buildscripts' / 'installer.map') as mapfile:
        Copier({
            'BITS': str(args.bits),
            'SRC': str(src_path.resolve()),
            'BUILD': str(args.build_dir.resolve()),
            'INST': str(installer_path.resolve()),
            'BUILD_CONFIG': 'Debug' if args.debug else 'Release',
            'PCBUILD_SUBDIR': 'amd64' if args.bits == 64 else 'win32'
        }).execute_script(mapfile)

    os.chdir(installer_path)

    bundle_name = get_bundle_name(args.bits)

    with ZipFile(f'pygmod-{bundle_name}.pyz', 'w') as installer_zip:
        installer_zip.write(src_path / 'python' /
                            'installer' / '__main__.py', '__main__.py')

        for bundle in ['common', bundle_name]:
            bundle_zip_name = f'{bundle}.zip'

            with ZipFile(bundle_zip_name, 'w') as bundle_zip:
                for file in [ent for ent in Path(bundle).rglob('*') if ent.is_file()]:
                    bundle_zip.write(file, file.relative_to(bundle))

            installer_zip.write(bundle_zip_name)


def get_bundle_name(bits: int):
    match sys.platform:
        case 'win32':
            return f'win{bits}'
        case 'linux':
            return f'linux{bits}'
        case _:
            logger.critical('Unknown platform')
            exit(1)


if __name__ == '__main__':
    main()
