from fastapi import APIRouter
from enum import Enum

from fastapi import Depends, Path
from sqlalchemy.orm import Session

from payments_app.adapters.database import get_db
from payments_app.routers.auth import get_current_active_user
from payments_app.schemas import TransactionCreate
from payments_app.crud import (
    create_transaction_item,
    get_all_transactions,
    get_transaction,
)
from payments_app.tasks import update_transaction_status


router = APIRouter(prefix="/transactions")


class Tags(Enum):
    transactions = "transactions"


@router.get(
    "",
    tags=[Tags.transactions],
    dependencies=[Depends(get_current_active_user)],
)
async def transactions_list(db: Session = Depends(get_db)):
    return get_all_transactions(db)


@router.get(
    "/{transaction_id}",
    tags=[Tags.transactions],
    dependencies=[Depends(get_current_active_user)],
)
async def transaction_detail(
    db: Session = Depends(get_db),
    transaction_id: int = Path(..., description="The ID of the transaction to get"),
):
    return get_transaction(db, transaction_id)


@router.post(
    "",
    tags=[Tags.transactions],
    status_code=201,
    dependencies=[Depends(get_current_active_user)],
)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    db_transaction = create_transaction_item(db, transaction)
    task_result = update_transaction_status.delay(db_transaction.id)
    return {"transaction": db_transaction, "task_id": task_result.id}
