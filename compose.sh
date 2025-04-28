#!/bin/bash


## Usage
#$ sudo ./compose.sh 'up' #Start the containers
#$ sudo ./compose.sh 'down' #Remove the container
#$ sudo ./compose.sh 'down --volumes' #Remove the containers volumes
#$ sudo ./compose.sh 'build' #Build the images
#$ sudo ./compose.sh 'build --no-cache' #Build without cache

(
source .env

command="docker compose"
if [ "$($command version | grep 'version v2')" = "" ]; then
    command=docker-compose
fi

if [ "$DEPLOYMENT_TYPE" == 'postgres' ]; then
    $command -f docker-compose-postgres.yml $1
elif [ "$DEPLOYMENT_TYPE" == 'postgres-ssl' ]; then
    $command -f docker-compose-postgres-ssl.yml $1
elif [ "$DEPLOYMENT_TYPE" == 'sqlite' ]; then
    $command -f docker-compose-sqlite.yaml $1
elif [ "$DEPLOYMENT_TYPE" == 'sqlite-ssl' ]; then
    $command -f docker-compose-sqlite-ssl.yaml $1
else
  echo "Please set DEPLOYMENT_TYPE env variable to on of 'postgres', 'postgres-ssl', 'sqlite', 'sqlite-ssl'"
fi
)

