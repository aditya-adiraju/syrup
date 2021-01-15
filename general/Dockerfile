FROM ubuntu:20.04
RUN dpkg --add-architecture i386
RUN apt-get update

# some nice defaults
RUN apt-get install -y ltrace strace socat gdb gcc netcat ssh sudo
# for grabbing source of glibc
RUN apt-get install -y libc6:i386 libc6-dbg glibc-source locales && tar -C /usr/src/glibc -xvf /usr/src/glibc/*.tar.xz

# for adding gef to gdb
RUN wget -q -O- https://github.com/hugsy/gef/raw/master/scripts/gef.sh | sh

### add additional tools you need to install here ###
# RUN apt-get install -y ...

# container configuration to set host user as guest user
ARG USER
RUN groupadd -g 1000 $USER  && useradd -g $USER -u 1000 -M $USER; exit 0 
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
RUN echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/user-nopasswd
WORKDIR /home/$USER
ENV TERM=xterm-color
CMD /bin/bash --login

