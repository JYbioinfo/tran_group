#!/bin/sh
# name:start_api
# start api, webstart
cd api
nohup gunicorn -c gunicorn.conf run:app 1>>API.log 2>>API.log &
echo $! >> ../service.pid
# nohup python run.py 1>>run.log 2>>run.log &

cd ../web
nohup gunicorn -c gunicorn.conf webstart:app 1>>Web.log 2>>Web.log &
echo $! >> ../service.pid