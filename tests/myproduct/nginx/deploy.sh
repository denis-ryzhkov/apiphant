#!/bin/bash
mkdir -p /opt/myproduct/public
grep myproduct-local.com /etc/hosts || echo '127.0.0.1 myproduct-local.com' | sudo tee -a /etc/hosts
sudo apt-get install --yes nginx
sudo ln -sf /opt/myproduct/nginx/myproduct /etc/nginx/sites-enabled/myproduct
sudo ln -sf /opt/myproduct/nginx/logrotate/nginx-myproduct /etc/logrotate.d/nginx-myproduct
/opt/myproduct/nginx/reload.sh
