#!/bin/bash

#run server
gunicorn -p gunicorn.pid --bind 0.0.0.0:$CCS_DAL_PORT --timeout=300 --workers=2 -k gevent server:api
