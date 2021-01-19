#!/bin/bash

# Build and run containers
docker-compose up -d --build

# Hack to wait for postgres container to be up before running alembic migrations
sleep 5;

# Run migrations
docker-compose run --rm backend alembic upgrade head

# Create superuser
docker-compose run --rm backend python3 app/create_superuser.py
