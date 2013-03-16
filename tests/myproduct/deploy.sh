#!/bin/bash
sudo mkdir -p /opt
sudo ln -sfT `pwd -P` /opt/myproduct
cd /opt/myproduct
mkdir -p log
for PART in api supervisor nginx;
do
    $PART/deploy.sh;
done
curl --data-binary '{"hello": "world"}' --request POST http://myproduct-local.com/api/v0/echo/read
