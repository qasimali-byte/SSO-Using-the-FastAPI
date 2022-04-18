#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username postgres --password faisal --dbname sso_idp <<-EOSQL
    CREATE USER postgres With PASSWORD 'faisal';
    CREATE DATABASE sso_idp;
    GRANT ALL PRIVILEGES ON DATABASE sso_idp TO postgres;

EOSQL