FROM python:3

# Download GarrysMod headers
RUN git clone https://github.com/Facepunch/gmod-module-base.git && \
    mv ./gmod-module-base/include/GarrysMod /usr/local/include/GarrysMod && \
    rm -rf ./gmod-module-base

COPY ./src/python/requirements.txt ./
RUN pip install --quiet --upgrade setuptools pip pytest pytest-cov pytest-pylint pytest-mock && \
    pip install --quiet --no-cache-dir -r requirements.txt
RUN rm requirements.txt

WORKDIR /usr/src/app
COPY . .

# Run tests
RUN cd ./src/python && \
    python -m pytest . ../../tests/python/
