#!/usr/bin/env bash
# a Bash script that sets up a web servers for the deployment of web_static

sudo apt-get update
sudo apt-get -y install nginx

mkdir -p /data/web_static/{shared,releases/test/}
echo "Welcome, Earthling!" > /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

if ! grep -q "location /hbnb_static/ {" /etc/nginx/sites-available/default
then
        sed -i "/server_name _;/a\\
        location /hbnb_static/ {\\
                alias /data/web_static/current/;\\
        }" /etc/nginx/sites-available/default
fi

sudo service nginx restart
