from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from sqlalchemy import text

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


@app.get("/healthcheck", status_code=status.HTTP_200_OK, dependencies=[Depends(get_db)])
async def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "OK", "database": "OK"}
    except Exception:
        return {"status": "ERROR", "database": "Failure"}
