#!/bin/bash
if sudo pgrep -l nginx;
    then sudo nginx -s reload;
    else sudo service nginx start;
fi
