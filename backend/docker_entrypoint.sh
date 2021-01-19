#!/usr/bin/env bash

set -e

if [[ $1 == 'serve' ]] ; then

    if [[ $2 == 'dev' ]] ; then

        wait-for-it postgres:5432 -- alembic upgrade head

    elif [[ $2 == 'prod' ]] ; then
        alembic upgrade head

    fi

    python app/main.py

else
    exec "$@"
fi
