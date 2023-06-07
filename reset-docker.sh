#!/bin/sh

docker rm agricola-postgres-1
docker rm agricola-redis-1

docker-compose up -d