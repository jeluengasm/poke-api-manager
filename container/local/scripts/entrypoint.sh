#!/usr/bin/env bash

set -o errexit
set -o pipefail
cmd="$@"

function postgres_ready(){
python << END
import sys
import psycopg2
import os

try:
    dbname = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT')
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError as e:
    print("Database connection failed. ", e)
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "DB not ready. Waiting..."
  sleep 1
done

>&2 echo "DB ready. Starting..."
exec $cmd
