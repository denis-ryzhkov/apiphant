#!/bin/bash
sudo mkdir -p /opt
sudo ln -sfT `pwd -P` /opt/myproduct
cd /opt/myproduct
mkdir -p log
for PART in api supervisor nginx;
do
    $PART/deploy.sh;
done
