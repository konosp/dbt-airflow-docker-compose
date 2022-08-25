#!/usr/bin/env bash

docker build -f ./dockerfile/dockerfile_ubuntu_china -t ubuntu-china:18.04 -t ubuntu-china:latest .
docker build -f ./dockerfile/dockerfile_airflow -t airflow:2.3.0 -t airflow:latest .
docker build -f ./dockerfile/dockerfile_dbt -t dbt-service:1.1.0 -t dbt-service:latest .
docker build -f ./dockerfile/dockerfile_hadoop -t hadoop:3.2.3 -t hadoop:latest .
docker build -f ./dockerfile/dockerfile_jupyter -t jupyter-spark:3.0.3 -t jupyter-spark:latest .
docker build -f ./dockerfile/dockerfile_spark -t spark:3.0.3 -t spark:latest .
docker build -f ./dockerfile/dockerfile_presto -t presto:0.261  -t presto:latest .