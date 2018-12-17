#!/bin/bash
cwd=${PWD}

echo "Creating virtual environment in ~/Env/uWsgiApps"
mkdir ${cwd}/../Env/
cd ${cwd}/../Env/
virtualenv -p python3 uWsgiApps

echo "Enabling virtualenv uWsgiApps"
source ./uWsgiApps/bin/activate

echo "Installing modules from requirements.txt"
cat epgapp/requirements.txt

cd ${cwd}
pip3 install -r epgapp/requirements.txt

echo "**************************************************"

echo "Enabling nginx site"
link=${PWD}/nginx/epgapp.kodibg.org
sudo ln -si $link /etc/nginx/sites-enabled/
echo `ls -la /etc/nginx/sites-enabled/epgapp.kodibg.org`

echo "Enabling uwsgi service"
link=${PWD}/service/uwsgi.service
sudo ln -si $link /etc/systemd/system/
echo `ls -la /etc/systemd/system/uwsgi.service`

echo "Creating temp folder"
mkdir -R epgapp/epgapp/temp/data/
chmod 755 epgapp/epgapp/temp/
chmod 755 epgapp/epgapp/temp/data/
chmod +x epgapp/epgapp/bin/wgmulti.exe
chmod +x epgapp/epgapp/bin/WebGrab+Plus.exe


echo "**************************************************"
echo "To start the service run sudo service uwsgi start"
echo "To see the service status run sudo service uwsgi status"
