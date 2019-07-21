#!/bin/bash

#py_ver = python3.6

clear

# Global Delay funtion because whynot?
DELAY()
{
	sleep 1;
}

# function check_python {
#   echo "Checking for python"
#   DELAY;
#   if [ ! -f $py_ver ]; then
#     echo "Install python 3.6 first!"
#     DELAY;
#     exit 1;
#   fi
#   echo "Python 3.6 present!"
#   DELAY;
# }

function install_depends()
{
  echo "Make sure you have pipenv installed or this won't work"
  DELAY;
  pipenv install --ignore-pipfile
  pipenv shell
  DELAY;
}

#check_python
install_depends
