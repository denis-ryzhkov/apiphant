#!/bin/bash
curl --data-binary '{"hello": "world"}' --request POST http://myproduct-local.com/api/v0/echo/read
