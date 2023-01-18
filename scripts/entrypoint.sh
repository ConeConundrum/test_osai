#!/bin/bash
export LOG_LEVEL
export SERVICE_PORT
export WORKER_COUNT

uvicorn app.main:app --host 0.0.0.0 --port "${SERVICE_PORT}" --log-level "${LOG_LEVEL,,}" --workers "${WORKER_COUNT:-1}"
