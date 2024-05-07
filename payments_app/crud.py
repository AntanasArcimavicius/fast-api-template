from fastapi import HTTPException
from sqlalchemy.orm import Session

from payments_app.models import Transaction as TransactionModel
from payments_app.schemas import TransactionCreate


class TransactionErrorException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(status_code=409, detail=detail)


def get_all_transactions(db: Session) -> list[TransactionModel]:
    transactions = db.query(TransactionModel).all()
    return transactions


def get_transaction(db: Session, transaction_id: int) -> TransactionModel | None:
    return (
        db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    )


def create_transaction_item(
    db: Session, transaction: TransactionCreate
) -> TransactionModel:
    try:
        db_transaction = TransactionModel(**transaction.model_dump())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        return db_transaction

    except Exception as e:
        db.rollback()
        raise TransactionErrorException(detail=f"Transaction failed: {e}")
