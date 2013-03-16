#!/bin/bash

echo Writing to server.log and client.log...

SERVER="apiphant myproduct 127.0.0.1:8888"
$SERVER >server.log 2>&1 &
sleep 1

/usr/bin/env python test.py >client.log 2>&1
pkill -f "$SERVER"

echo ...
tail server.log
echo ...
tail client.log
