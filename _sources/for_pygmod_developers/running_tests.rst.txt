Running Unit tests
==================

Requirements
------------

Windows
^^^^^^^

1. `Docker Desktop for Windows <https://hub.docker.com/editions/community/docker-ce-desktop-windows>`_

Linux
^^^^^

1. **Docker** (``docker.io`` package on Debian-based distributions, ``docker`` package on Arch-based distributions)

Instructions
------------

Python tests
^^^^^^^^^^^^

1. Run in a command prompt from the repository root::

    docker build -f python_tests.Dockerfile .

C++ tests
^^^^^^^^^

1. Run in a command prompt from the repository root::

    docker build -f cpp_tests.Dockerfile .
