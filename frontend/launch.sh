#! /bin/bash

sudo npm run build
sudo systemctl stop sensorApi
sudo systemctl stop nginx
sudo systemctl start sensorApi
sudo systemctl start nginx
