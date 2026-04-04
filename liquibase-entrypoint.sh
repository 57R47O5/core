#!/bin/sh
set -e

# Defaults
CLASSPATH="/liquibase/classpath/postgresql-42.7.8.jar"
CHANGELOG="/changelog/generated/elecciones/master.yaml"
URL="jdbc:postgresql://db:5432/${DB_NAME}"

# Ejecutar liquibase con defaults + comando recibido
liquibase \
  --classpath=$CLASSPATH \
  --url=$URL \
  --username=$DB_USER \
  --password=$DB_PASSWORD \
  --changeLogFile=$CHANGELOG \
  "$@"