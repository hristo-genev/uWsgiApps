#!/bin/bash
cwd=${PWD}

echo "Creating virtual environment in ~/Env/uWsgiApps"
mkdir ${cwd}/../Env/
cd ${cwd}/../Env/
virtualenv -p python3.6 uWsgiApps

echo "Enabling virtualenv uWsgiApps"
source ./uWsgiApps/bin/activate

echo "Installing modules from requirements.txt"
cat epgapp/requirements.txt

cd ${cwd}
pip3 install -r epgapp/requirements.txt

echo "**************************************************"

echo "Configuring nginx"
echo "Setting server_names_hash_bucket_size 64;"
sed -i 's/#\ server_names_hash_bucket_size\ 64;/server_names_hash_bucket_size\ 64;/gi' /etc/nginx/nginx.conf

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

echo "Restarting nginx server"
sudo service nginx restart

echo "Enabling uwsgi service"
link=${PWD}/service/uwsgi.service
sudo ln -sif $link /etc/systemd/system/
echo `ls -la /etc/systemd/system/uwsgi.service`

echo "Creating temp folder"
mkdir -p epgapp/epgapp/temp/data/ -m 755
mkdir -p epgapp/epgapp/logs/ -m 755
touch epgapp/logs/debug.txt
chmod +x epgapp/epgapp/bin/wgmulti.exe
chmod +x epgapp/epgapp/bin/WebGrab+Plus.exe


echo "**************************************************"
echo "To start the service run \"sudo service uwsgi start\""
echo "To see the service status run \"sudo service uwsgi status\""
