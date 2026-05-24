from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.database import create_db_and_tables
from routers import auth, items


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Include modular sub-routers
app.include_router(auth.router)
app.include_router(items.router)