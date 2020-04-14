FROM i386/debian

RUN apt update && apt install -y g++ make cmake python3-dev git
WORKDIR /build
COPY . .
RUN cmake . && make
RUN tar -cf out.tar *.so *.dll
