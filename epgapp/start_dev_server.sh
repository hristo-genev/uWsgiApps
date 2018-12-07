#!/bin/bash -e

cd ~/uWsgiApps/epgapp/
source ~/Env/epgapp/bin/activate && ~/Env/epgapp/bin/uwsgi --http :9981 --wsgi-file epgapp/wsgi.py --stats :9982
