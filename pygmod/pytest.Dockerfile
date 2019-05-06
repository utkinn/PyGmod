# This Dockerfile builds and tests the Python extension
# Python tests are run using pytest
# C++ tests are run using Google Test (TODO)

FROM python:3

WORKDIR /usr/src/app

RUN git clone https://github.com/Facepunch/gmod-module-base.git && \
    mv ./gmod-module-base/include/GarrysMod /usr/local/include/GarrysMod && \
    rm -rf ./gmod-module-base

COPY requirements.txt ./
RUN pip install --quiet --upgrade setuptools pip && \
    pip install --quiet --no-cache-dir -r requirements.txt || exit 1

COPY . .

RUN python setup.py test || exit 1
