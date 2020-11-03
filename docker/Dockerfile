# Dockerfile to build DMTCP image
FROM centos:7
MAINTAINER Lei Pan <leipan@jpl.nasa.gov>
LABEL description="DMTCP container" \
      Version=1.0.0 \
      Vendor="JPL"

USER root

RUN yum -y update && yum -y --setopt=tsflags=nodocs install    \
      gcc-c++                                   \
      build-essential                           \
      git-core                                  \
      make                                      \
      vim                                       \
      python3-pip python3-dev                   \
      && yum clean all                          \
      && cd /usr/local/bin                      \
      && ln -s /usr/bin/python3 python          \
      && pip3 install --upgrade pip

RUN set -ex \
    && useradd -ms /bin/bash leipan             \
    && echo "export PATH=$PATH:/home/leipan/local/dmtcp_installation/bin" >> /home/leipan/.bashrc \
    && echo "alias ll='ls -alF'" >> /home/leipan/.bashrc \
    && echo "alias rm='rm -i'"   >> /home/leipan/.bashrc \
    && echo "alias mv='mv -i'"   >> /home/leipan/.bashrc \
    && echo "alias cp='cp -i'"   >> /home/leipan/.bashrc \
    && echo "alias h='history'"  >> /home/leipan/.bashrc

USER leipan
RUN mkdir -p /home/leipan/dmtcp
RUN mkdir -p /home/leipan/local/dmtcp_installation
RUN mkdir -p /home/leipan/navp
WORKDIR /home/leipan/dmtcp

RUN git clone https://github.com/dmtcp/dmtcp.git /home/leipan/dmtcp && \
      git checkout master &&                    \
      git log -n 1
RUN git clone https://leipan:e47e4b23ab852c2ba732260183b12033ad591018@github.com/leipan/navp.git /home/leipan/navp

RUN ./configure --prefix=/home/leipan/local/dmtcp_installation && make -j 2 && make install

ENTRYPOINT ["bash"]
