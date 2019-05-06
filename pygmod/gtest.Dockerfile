FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y g++ cmake libgtest-dev git python3-dev

# Download GarrysMod headers
RUN git clone https://github.com/Facepunch/gmod-module-base.git && \
    mv ./gmod-module-base/include/GarrysMod /usr/local/include/GarrysMod && \
    rm -rf ./gmod-module-base

# Compile GTest
RUN cd /usr/src/gtest && \
    cmake CMakeLists.txt && \
    make && \
    cp *.a /usr/lib

WORKDIR /usr/src/app
COPY . .

# Compile & run tests
RUN cmake CmakeLists.txt && make
RUN ./run_gtests || exit 1

