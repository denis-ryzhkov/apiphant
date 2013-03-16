#!/bin/bash
sudo apt-get install --yes supervisor
sudo ln -sf /opt/myproduct/supervisor/myproduct.conf /etc/supervisor/conf.d/myproduct.conf
/opt/myproduct/supervisor/reload.sh
