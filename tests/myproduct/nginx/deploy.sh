#!/bin/bash
mkdir -p /opt/myproduct/public
grep myproduct-local.com /etc/hosts || sudo echo '127.0.0.1 myproduct-local.com' >>/etc/hosts
sudo apt-get install --yes nginx
sudo ln -sf /opt/myproduct/nginx/myproduct /etc/nginx/sites-enabled/myproduct
sudo ln -sf /opt/myproduct/nginx/logrotate/nginx-myproduct /etc/logrotate.d/nginx-myproduct
if sudo pgrep -l nginx;
    then sudo nginx -s reload;
    else sudo service nginx start;
fi
