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
      gdb                                       \
      wget                                      \
      m4                                        \
      centos-release-scl                        \
      python3-pip python3-dev                   \
      && yum clean all                          \
      && cd /usr/local/bin                      \
      && ln -s /usr/bin/python3 python          \
      && pip3 install --upgrade pip             \
      && pip3 install numpy                     \
      && pip3 install pykdtree

RUN set -ex \
    && useradd -ms /bin/bash leipan             \
    && echo "export PATH=$PATH:/home/leipan/local/dmtcp_installation/bin" >> /home/leipan/.bashrc \
    && echo "export DMTCP_ROOT=/home/leipan/local/dmtcp_installation/" >> /home/leipan/.bashrc \
    && echo "alias ll='ls -alF'" >> /home/leipan/.bashrc \
    && echo "alias rm='rm -i'"   >> /home/leipan/.bashrc \
    && echo "alias mv='mv -i'"   >> /home/leipan/.bashrc \
    && echo "alias cp='cp -i'"   >> /home/leipan/.bashrc \
    && echo "alias h='history'"  >> /home/leipan/.bashrc

USER leipan
RUN mkdir -p /home/leipan/dmtcp
RUN mkdir -p /home/leipan/local/dmtcp_installation
RUN mkdir -p /home/leipan/navp

WORKDIR /home/leipan
USER root
RUN yum -y install devtoolset-7 ; scl enable devtoolset-7 bash
SHELL [ "/usr/bin/scl", "enable", "devtoolset-7"]

# install bison for glibc 2.28
RUN wget https://ftp.gnu.org/gnu/bison/bison-3.2.tar.gz
RUN tar xf bison-3.2.tar.gz
RUN mkdir $HOME/install-bison
RUN cd bison-3.2; ./configure --prefix=$HOME/install-bison; make; make install

# install make for glibc 2.28
RUN wget https://ftp.gnu.org/gnu/make/make-4.3.tar.gz
RUN tar xzf make-4.3.tar.gz
RUN mkdir $HOME/install-make; cd make-4.3; ./configure --prefix=$HOME/install-make; make; make install
RUN export PATH=$HOME/install-make/bin:$HOME/install-bison/bin:$PATH

# download glibc 2.28
RUN wget http://ftp.gnu.org/gnu/glibc/glibc-2.28.tar.gz
RUN tar -xzf glibc-2.28.tar.gz

# RUN export PATH=$HOME/install/bin:$PATH
# RUN echo $PATH
# RUN ls $HOME/install-bison/bin
RUN yum -y install gettext texinfo
RUN export PATH=$HOME/install-make/bin:$HOME/install-bison/bin:$PATH; cd glibc-2.28; mkdir build; cd build; ../configure CC=/opt/rh/devtoolset-7/root/bin/gcc CXX=/opt/rh/devtoolset-7/root/bin/g++ --with-headers=/usr/include --with-binutils=/usr/bin --prefix=/usr; make; make install; exit 0

USER leipan
WORKDIR /home/leipan/dmtcp

RUN git clone https://github.com/dmtcp/dmtcp.git /home/leipan/dmtcp && \
      git checkout master &&                    \
      git log -n 1
RUN git clone https://leipan:e47e4b23ab852c2ba732260183b12033ad591018@github.com/leipan/navp.git /home/leipan/navp

RUN ./configure --enable-debug CC=/opt/rh/devtoolset-7/root/bin/gcc CXX=/opt/rh/devtoolset-7/root/bin/g++ --prefix=/home/leipan/local/dmtcp_installation && make -j clean && make -j8 && make install

ENTRYPOINT ["/bin/bash"]
