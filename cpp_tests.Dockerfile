FROM alpine

RUN apk add --no-cache g++ make cmake gtest gtest-dev git python3-dev

# Download GarrysMod headers
RUN git clone https://github.com/Facepunch/gmod-module-base.git && \
    mv ./gmod-module-base/include/GarrysMod /usr/include/GarrysMod && \
    rm -rf ./gmod-module-base

WORKDIR /cpp-tests
COPY . .

# Compile & run tests
RUN cd ./tests/cpp && \
    cmake . && \
    make && \
    ./run_gtests || exit 1
