# Dockerfile to build DMTCP container images.
### FROM ubuntu:15.04
FROM ubuntu:20.04
MAINTAINER Lei Pan <leipan@jpl.nasa.gov>

RUN apt-get update -q && apt-get -qy install    \
      build-essential                           \
      git-core                                  \
      make                                      \
      vim                                       \
      python3-pip python3-dev                   \
      && cd /usr/local/bin                      \
      && ln -s /usr/bin/python3 python          \
      && pip3 install --upgrade pip

RUN mkdir -p /dmtcp
RUN mkdir -p /tmp

WORKDIR /dmtcp
RUN git clone https://github.com/dmtcp/dmtcp.git /dmtcp && \
      git checkout master &&                    \
      git log -n 1
RUN git clone https://leipan:e47e4b23ab852c2ba732260183b12033ad591018@github.com/leipan/navp.git /tmp

RUN ./configure --prefix=/usr && make -j 2 && make install

ENTRYPOINT ["bash"]
