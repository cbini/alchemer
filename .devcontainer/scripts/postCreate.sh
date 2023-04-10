#!/bin/bash

# update/install apt packages
sudo apt-get -y --no-install-recommends update &&
  sudo apt-get -y --no-install-recommends upgrade &&
  sudo apt-get -y --no-install-recommends install bash-completion &&
  sudo apt-get -y autoremove &&
  sudo apt-get -y clean

# create env folder
mkdir -p ./env

# update pip
python -m pip install --no-cache-dir --upgrade pip
