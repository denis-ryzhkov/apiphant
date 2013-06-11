#!/bin/bash
sudo apt-get install --yes supervisor
sudo adduser --system --group --disabled-login --home /opt/myproduct --no-create-home myproduct
sudo ln -sf /opt/myproduct/supervisor/myproduct.conf /etc/supervisor/conf.d/myproduct.conf
/opt/myproduct/supervisor/reload.sh
