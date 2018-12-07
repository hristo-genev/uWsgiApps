#!/bin/bash

echo "Enabling nginx site"
link=${PWD}/nginx/epgapp.kodibg.org
sudo ln -si $link /etc/nginx/sites-enabled/
echo `ls -la /etc/nginx/sites-enabled/epgapp.kodibg.org`

echo "Enabling uwsgi service"
link=${PWD}/service/uwsgi.service
sudo ln -si $link /etc/systemd/system/
echo `ls -la /etc/systemd/system/uwsgi.service`
