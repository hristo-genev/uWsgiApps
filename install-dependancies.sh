#!/bin/sh

sudo apt install -y gnupg ca-certificates
sudo apt update

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list

# Python new versions repo
sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update
sudo apt-get -y upgrade

# Remove redundant packages
sudo apt remove -y apache2

# Install required packages
sudo apt-get -y install python python3 python3-pip python-virtualenv python-lxml python3-lxml libxml2-dev libxslt-dev python-dev nginx php php-fpm
sudo apt-get -y install gcc mono-devel build-essential software-properties-common

