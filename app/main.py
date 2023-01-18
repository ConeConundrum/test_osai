from fastapi import FastAPI

from app.api.main_api import api_router
from app.db.database import get_connection_pool, make_migrations, initiate_db
from app.settings.config import config
from app.settings.logging import logger


app = FastAPI(title=config.SERVICE_NAME, version=config.VERSION)
app.include_router(api_router)


@app.on_event("startup")
async def db_setup_at_startup():
    await initiate_db()
    # make_migrations()
    app.state.db = await get_connection_pool()
    logger.info("Server Startup")


@app.on_event("shutdown")
async def db_close_at_shutdown():
    if app.state.db:
        await app.state.db.close()
    logger.info("Server Shutdown")

