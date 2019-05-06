# Contributing to PyGmod

## Python Extension

The Python extension and related packages are contained in ``/pygmod/``. Docker containers have been provided for running tests:

```
pytest.Dockerfile	for testing the Python code
gtest.Dockerfile	for testing the C++ code
```

They can be built and run like so:
```
docker build -f pytest.Dockerfile .
docker build -f gtest.Dockerfile .
```
