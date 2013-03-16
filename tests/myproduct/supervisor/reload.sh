#!/bin/bash
if sudo pgrep -l supervisord;
    then sudo supervisorctl reload;
    else sudo service supervisor start;
fi
sleep 7
sudo supervisorctl status
curl --data-binary '{"hello": "world"}' --request POST http://myproduct-local.com/api/v0/echo/read
