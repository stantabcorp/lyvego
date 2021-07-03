#!/bin/bash

sudo docker ps -a -q  --filter ancestor=lyvego
sudo docker rmi lyvego --force && sudo docker-compose build && sudo docker-compose up -d