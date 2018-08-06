from distutils.core import setup
from Cython.Build import cythonize

# distutils: language = c++

setup(
    name = 'GPython',
    version = '0.1.0-alpha',
    ext_modules = cythonize("luastack.pyx"),
)
