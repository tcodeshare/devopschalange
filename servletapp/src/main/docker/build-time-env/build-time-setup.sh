#!/bin/bash
export PATH=${PATH}:/opt/ubs/jdk1.8.0_192/bin:/opt/ubs/apache-maven-3.5.4/bin
export JAVA_HOME=/opt/ubs/jdk1.8.0_192

# Change dir for docker builds
if [ -f  /.dockerenv ] ; then
    cd /workspace
    dir=$(pwd)
    echo "[EXE]: /opt/ubs/apache-maven-3.5.4/bin/mvn $@ in $dir"
    /opt/ubs/apache-maven-3.5.4/bin/mvn "$@"
fi

