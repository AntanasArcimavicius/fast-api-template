from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from payments_app.adapters.database import engine, get_db
from payments_app.models import Base
from payments_app.routers import auth, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(transactions.router)


class DbConnectionErrorException(Exception):
    def __init__(self, message: str):
        self.message = message


@app.exception_handler(DbConnectionErrorException)
async def db_exception_handler(request: Request, exc: DbConnectionErrorException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "ERROR", "database": exc.message},
    )


@app.get("/healthcheck", status_code=status.HTTP_200_OK, dependencies=[Depends(get_db)])
async def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "OK", "database": "OK"}
    except OperationalError:
        raise DbConnectionErrorException("Connection failed")
