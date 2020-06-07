FROM python:alpine

COPY ./src/python/requirements.txt ./
RUN pip install --quiet --no-cache-dir --upgrade setuptools pip pytest pytest-cov pytest-pylint pytest-mock
RUN pip install --quiet --no-cache-dir -r requirements.txt && \
    rm requirements.txt

WORKDIR /python-tests
COPY . .

# Run tests
RUN cd ./src/python && \
    python -m pytest . ../../tests/python/
