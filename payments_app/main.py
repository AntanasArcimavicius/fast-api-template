from contextlib import asynccontextmanager

from fastapi import FastAPI

from payments_app.adapters.database import engine
from payments_app.models import Base
from payments_app.routers import auth, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(transactions.router)
