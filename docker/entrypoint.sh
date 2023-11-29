#!/bin/bash

APP_TYPE=${APP_TYPE:-"ingest"}

case $APP_TYPE in

  "ingest")
    echo "Starting 'ingest' script"
    python3 /app/ingest.py -b $APP_BUCKET -t $APP_TABLE -d $APP_DATE
    ;;

  "transform")
    echo "Starting 'transform' script"
    python3 /app/transform_data.py -b $APP_BUCKET -d $APP_DATE
    ;;
esac