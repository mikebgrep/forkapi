#!/bin/bash


# Install Docker
apt update
apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"  --noinput
apt-cache policy docker-ce
apt -y install docker-ce

# Install ssl
apt -y install certbot python3-certbot-nginx
read -p "Enter domain name connected to the droplet: " domain_name
certbot --nginx -d domain_name


