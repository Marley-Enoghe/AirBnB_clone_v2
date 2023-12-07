#!/usr/bin/env bash
# a Bash script that sets up a web servers for the deployment of web_static

# install NGINX if not installed
if ! command -v nginx &> /dev/null
then
        sudo apt update
        sudo apt install nginx
        sudo service nginx start
else
        echo "NGINX is already installed"
fi

mkdir -p /data/web_static/{shared,releases/test/}
echo "Welcome, Earthling!" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

if ! grep -q "location /hbtn_static/ {" /etc/nginx/sites-available/default
then
        sed -i "/server_name _;/a\\
        location /hbtn_static/ {\\
                alias /data/web_static/current/;\\
                autoindex off;\\
        }" /etc/nginx/sites-available/default
fi

sudo service nginx restart
