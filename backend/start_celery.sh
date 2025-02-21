#!/bin/bash

celery -A main.celery worker --loglevel=info &

# SAVE PID CELERY
CELERY_PID=$!

echo "Waiting for Celery"
while ! celery -A main.celery status > /dev/null 2>&1; do
  sleep 2
done

echo "Celery OK!"

# run task monitor filesystem
python -c "from app import monitor; monitor.delay('data/')"

wait $CELERY_PID