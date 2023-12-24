#!/bin/bash
set -e

# Custom code to load the SQL dump
echo "Loading SQL dump..."
psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < /usr/local/bin/dump.sql

# Call the original entrypoint script
exec docker-entrypoint.sh postgres
