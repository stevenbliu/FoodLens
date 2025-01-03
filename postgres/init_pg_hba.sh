#!/bin/bash
echo "Starting pg_hba initialization script..."

# Start PostgreSQL (if not already running)
# echo "Starting PostgreSQL..."
# pg_ctl start -D /var/lib/postgresql/data

# Wait until PostgreSQL is ready for connections
# until pg_isready -h localhost -p 5432; do
until pg_isready -h /var/run/postgresql -p 5432; do

    echo "Waiting for PostgreSQL to start..."
    sleep 1
done

# Append new pg_hba.conf rules directly
echo "host    all     all     172.18.0.0/16    md5" >> /var/lib/postgresql/data/pg_hba.conf
echo "host    replication     all     172.18.0.0/16    md5" >> /var/lib/postgresql/data/pg_hba.conf
echo "host    replication     replication_user     0.0.0.0/0    md5" >> /var/lib/postgresql/data/pg_hba.conf

# Reload PostgreSQL to apply changes
pg_ctl reload
