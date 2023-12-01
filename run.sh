#!/bin/bash

set -eu

HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-2}
UVICORN_WORKER=${UVICORN_WORKER:-"uvicorn.workers.UvicornWorker"}
GRACEFUL_TIMEOUT=${GRACEFUL_TIMEOUT:-300}
APP_NAME=${APP_NAME:-"src.app.app:app"}

gunicorn ${APP_NAME} \
    -b ${HOST}:${PORT} \
    -w ${WORKERS} \
    -k ${UVICORN_WORKER} \
    --graceful-timeout ${GRACEFUL_TIMEOUT} \
    --reload