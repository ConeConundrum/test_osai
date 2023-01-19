#!/bin/bash
export LOG_LEVEL
export SERVICE_PORT
export WORKER_COUNT

python -c "import asyncio; from app.database.database import initiate_db; asyncio.get_event_loop().run_until_complete(initiate_db());"
python -c "from app.migrations.migrations import make_migrations; make_migrations();"

uvicorn app.main:app --host 0.0.0.0 --port "${SERVICE_PORT}" --log-level "${LOG_LEVEL,,}" --workers "${WORKER_COUNT:-1}"
