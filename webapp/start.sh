#!/usr/bin/env bash

platform='unknown'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   platform='linux'
   /usr/bin/python djangoserver.py &
   /usr/bin/python roaster.py
elif [[ "$unamestr" == 'Darwin' ]]; then
   platform='osx'
   /usr/local/Cellar/python/2.7.14_2/libexec/bin/python djangoserver.py &
   /usr/local/Cellar/python/2.7.14_2/libexec/bin/python roaster.py
fi
