#!/bin/bash
app="docker.3b"
docker build -t ${app}:latest .
docker run -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}