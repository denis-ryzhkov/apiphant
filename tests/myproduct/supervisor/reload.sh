#!/bin/bash
if sudo pgrep -l supervisord;
    then sudo supervisorctl reload;
    else sudo service supervisor start;
fi
sleep 7
sudo supervisorctl status
