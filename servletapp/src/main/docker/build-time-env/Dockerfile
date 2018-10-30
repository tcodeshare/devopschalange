##==============================================================================
## BRIEF:       Base image for JDK Development
##==============================================================================
FROM  centos:7.5.1804
LABEL maintainer="tcodeshare <tcodeshare@44616261+tcodeshare@users.noreply.github.com>"

#-------------------------------------------------------------------------------
# Predefined variables
#-------------------------------------------------------------------------------
ENV DEVENV_ROOT="/opt/ubs"
ENV DEVENV_WORKSPACE="/workspace"
RUN mkdir --parents ${DEVENV_ROOT}/bin && \
    mkdir --parents ${DEVENV_WORKSPACE}

#-------------------------------------------------------------------------------
# Access over proxy
#-------------------------------------------------------------------------------
RUN test ! -z "$http_proxy" && echo "proxy=$http_proxy" >> /etc/yum.conf || :

#-------------------------------------------------------------------------------
# Setup YUM repos
#-------------------------------------------------------------------------------
# install supporting tools
RUN yum -y install  epel-release \
    wget
RUN yum clean all;

#-------------------------------------------------------------------------------
# Install JDK
#-------------------------------------------------------------------------------
ENV JAVA_MAJOR_VERSION=8u192
ENV JAVA_ENV_VERSION=1.8.0_192
ENV JAVA_VERSION=${JAVA_MAJOR_VERSION}-ea-bin-b04-linux-x64-01_aug_2018

RUN wget -q --no-cookies --no-check-certificate \
    --header "Cookie: oraclelicense=accept-securebackup-cookie" \
    -O /tmp/jdk.tar.gz \
    https://download.java.net/java/jdk${JAVA_MAJOR_VERSION}/archive/b04/binaries/jdk-${JAVA_VERSION}.tar.gz  && \
    tar zxfv /tmp/jdk.tar.gz -C  ${DEVENV_ROOT}
    
#-------------------------------------------------------------------------------
# Install Maven
#-------------------------------------------------------------------------------
ENV MAVEN_VERSION=3.5.4
ENV JAVA_HOME /opt/ubs/jdk1.8.0_192
RUN wget -q --no-cookies --no-check-certificate \
    -O /tmp/maven.tar.gz \
    http://ftp.man.poznan.pl/apache/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz && \
    tar zxfv /tmp/maven.tar.gz -C  ${DEVENV_ROOT}

ADD build-time-setup.sh ${DEVENV_ROOT}/bin
RUN chmod +x ${DEVENV_ROOT}/bin/*

#-------------------------------------------------------------------------------
# Install Docker Compose
#-------------------------------------------------------------------------------
RUN curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" \
    -o ${DEVENV_ROOT}/bin/docker-compose

#-------------------------------------------------------------------------------
# Package env
#-------------------------------------------------------------------------------
RUN tar cfv /devenv.tar ${DEVENV_ROOT} 

#-------------------------------------------------------------------------------
# Create image from scratch so it not contains temp deps
#-------------------------------------------------------------------------------
#FROM centos:7.5.1804
ENV PATH ${PATH}:${DEVENV_ROOT}/bin:${DEVENV_ROOT}/apache-maven-${MAVEN_VERSION}/bin
#COPY --from=0 /devenv.tar /
#RUN tar xfv /devenv.tar ${DEVENV_ROOT} 

CMD /opt/ubs/bin/build-time-setup.sh package
#ENTRYPOINT /opt/ubs/bin/build-time-setup.sh
