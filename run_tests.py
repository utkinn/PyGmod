import sys
from shutil import copyfile
from os import remove

LUASTACK_PATH = 'python_extensions\\luastack.py'

sys.path.insert(0, 'python_extensions')

copyfile('tests\\luastack_mock.py', LUASTACK_PATH)

try:
    import tests
finally:
    remove(LUASTACK_PATH)
