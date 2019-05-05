# Contributing to PyGmod

PyGmod is split up into two main sections: Python code and C++ code.

The C++ code is made up of a Garry's Mod addon and some extensions to Python. The Python code is the ``gmod.api`` module which exposes Garry's Mod Lua functions, and an internal ``pygmod`` module.

## Python Code

Located in ``/src/python/``, ``python_tests.Dockerfile`` is provided for running tests (located in ``/tests/python/``):

```
docker build -f python_tests.Dockerfile .
```

## C++ Code

Located in ``/src/cpp/``, ``cpp_tests.Dockerfile`` is provided for running tests (located in ``/tests/cpp/``):

```
docker build -f cpp_tests.Dockerfile .
```
