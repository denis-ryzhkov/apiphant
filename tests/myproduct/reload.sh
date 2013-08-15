#!/bin/bash
cd /opt/myproduct
for PART in supervisor nginx
do
    $PART/reload.sh
done
sleep 2
./quick-test.sh
