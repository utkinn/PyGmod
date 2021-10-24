#!/usr/bin/env python3

"""Copies files from one path to another. Paths are read from a "map file" supplied as an argument."""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import re
import logging
from pathlib import Path
import glob
import shutil
import sys
from typing import TextIO

__all__ = ['Copier']

logging.basicConfig(level=logging.INFO)


def main() -> None:
    argp = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description='''Copies files from one path to another. Paths are read from a "map file" supplied as an argument.

Mapfile contains mappings from source path to destination path, each mapping being on a separate line
and source and destination paths separated by ' -> ' (with at least one whitespace symbol surrounding the arrow from both sides).
Path components are separated by '/' on all OSes.
If the destination path ends with a slash, it is interpreted as a directory and will be created if it does not exist.
Glob patterns such as '*' and '**' are supported.

Whitespace symbols at line beginnings are ignored.
Lines starting with '#' are treated as comment lines and are ignored. Comments can be inline, but in this case '#' should be separated from the destination path by at least one space.

You can use the -d option when invoking the script to define variables. Variables are defined in a form "VAR=value" (no spaces around "=").
To substitute a variable in the map file, use "${VAR}".

Mappings can be conditional. Condition clause has the following form:

    !if VAR = value
        # Paths
    !endif

Condition clauses can not be nested.

There is one predefined variable - PLATFORM, which matches sys.platform value.

A !del command can be use to selectively remove redundant copied files.

    !del C:\\Windows\\System32\\

# Example mapfile
dir1                -> dir2             # Copy dir1 with its contents to dir2
dir3/file.txt       -> dir2/myfile.txt  # Copy a file with renaming
dir3/test.txt       -> dir2             # Copy a file without renaming
dir4/*.txt          -> dir5             # Copy all text files...
dir4/**/*.txt       -> dir5             # ...recursively
!if COPY_COOKIES = yes
    ${HOME}/cookies.txt -> /tmp         # Variable "HOME" gets substituted
!endif
        ''')
    argp.add_argument('mapfile', type=open, help='Mapfile path')
    argp.add_argument('-v', '--var', type=variable_dict, action='append',
                      help='Define variables, i. e. MY_PATH=/tmp', dest='vars')

    args = argp.parse_args()

    Copier(args.vars).execute_script(args.mapfile)


def variable_dict(vars: list[str]):
    result = {}
    for var in vars:
        k, v = var.split('=', 1)
        result[k] = v
    return result


class Copier:
    _condition = None

    def __init__(self, vars: tuple[str, str]):
        self._vars = vars

    def execute_script(self, mapfile: TextIO) -> None:
        self._vars['PLATFORM'] = sys.platform

        line: str
        for line in mapfile:
            line = substitute_vars(
                re.sub(r'\s+#.*$', '', line.strip()), self._vars)

            if line.startswith('#') or not line:
                continue

            if self._handle_condition_command(line):
                continue

            if not self._condition_holds_true():
                logging.debug('Skipping "%s" because %s != %s',
                              line, *self._condition)
                continue

            if self._handle_del_command(line):
                continue

            self._handle_path_mapping(line)

    def _condition_holds_true(self):
        return not self._condition or self._vars[self._condition[0]] == self._condition[1]

    def _handle_condition_command(self, line: str) -> bool:
        if cond_match := re.fullmatch(r'!if\s+(?P<var>.*?)\s*==\s*(?P<value>.*?)', line):
            if self._condition:
                logging.error('Nested conditions are not supported')
                exit(1)

            var_name = cond_match.group('var')
            if var_name not in self._vars:
                logging.debug('Vars: %s', self._vars)
                logging.critical(
                    'Unknown variable in conditional: "%s"', var_name)
                exit(1)

            self._condition = (var_name, cond_match.group('value'))
            return True

        if line == '!endif':
            self._condition = None
            return True

        return False

    def _handle_del_command(self, line: str) -> bool:
        if del_match := re.fullmatch(r'!del\s+(?P<path>.*)', line):
            paths = map(Path, glob.glob(del_match.group('path')))
            for path in paths:
                logging.info('Deleting %s', path)
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)
            return True
        return False

    def _handle_path_mapping(self, line: str) -> None:
        match = re.fullmatch(
            r'(?P<src>.*?)\s+->\s+(?P<dest>.*)', line)
        if not match:
            logging.critical('Failed to parse line:\n    %s', line)
            exit(1)

        srcs = map(Path, glob.glob(match.group('src').strip()))
        dest = Path(match.group('dest').strip())

        if match.group('dest').endswith('/'):
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)

        for src in srcs:
            logging.info(f'%s -> %s', src, dest)
            if src.is_file():
                if dest.is_dir():
                    shutil.copyfile(src, dest / src.name)
                else:
                    shutil.copyfile(src, dest)
            else:
                shutil.copytree(src, dest / src.name, dirs_exist_ok=True)


def substitute_vars(line: str, vars: dict[str, str]) -> str:
    for key, value in vars.items():
        line = line.replace(f'${{{key}}}', value)
        logging.debug('Replaced %s with %s: %s', key, value, line)

    if '${' in line:
        logging.critical('Some variables left unsubstituted:\n    %s', line)
        exit(1)

    return line


if __name__ == '__main__':
    main()
