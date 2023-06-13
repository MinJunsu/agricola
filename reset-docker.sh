#!/bin/sh

docker rm -f `docker ps -a -q`
docker rmi -f `docker images`
docker volume rm -f `docker volume ls`

docker-compose up -d