FROM python:3

# Download GarrysMod headers
RUN git clone https://github.com/Facepunch/gmod-module-base.git && \
    mv ./gmod-module-base/include/GarrysMod /usr/local/include/GarrysMod && \
    rm -rf ./gmod-module-base

COPY requirements.txt ./
RUN pip install --quiet --upgrade setuptools pip && \
    pip install --quiet --no-cache-dir -r requirements.txt || exit 1
RUN rm requirements.txt

WORKDIR /usr/src/app
COPY . .

# Run tests
RUN python setup.py test || exit 1
