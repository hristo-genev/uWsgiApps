#!/bin/bash
cwd=${PWD}

echo "Installing Mono"
#https://www.mono-project.com/download/stable/#download-lin-ubuntu
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
sudo apt update
sudo apt install mono-devel -Y

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

echo "Enabling nginx sites"
link=${PWD}/nginx/epgapp.kodibg.org
sudo ln -sif $link /etc/nginx/sites-enabled/
echo `ls -la /etc/nginx/sites-enabled/epgapp.kodibg.org`

link=${PWD}/nginx/freetvandradio.kodibg.org
sudo ln -sif $link /etc/nginx/sites-enabled/
echo `ls -la /etc/nginx/sites-enabled/freetvandradio.kodibg.org

link=${PWD}/nginx/proxy.kodibg.org
sudo ln -sif $link /etc/nginx/sites-enabled/
echo `ls -la /etc/nginx/sites-enabled/proxy.kodibg.org

echo "Enabling uwsgi service"
link=${PWD}/service/uwsgi.service
sudo ln -sif $link /etc/systemd/system/
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
