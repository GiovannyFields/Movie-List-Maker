from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import create_tables
from backend.routers import lists, movies, suggestions


# runs once when the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Movie List Maker API", lifespan=lifespan)

# each router file holds the endpoints for one thing
app.include_router(lists.router)
app.include_router(movies.router)
app.include_router(suggestions.router)
