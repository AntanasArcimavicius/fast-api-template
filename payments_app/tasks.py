from payments_app.adapters.database import SessionLocal
from payments_app.adapters.ques import app

from payments_app.models import Transaction, TransactionStatus


@app.task
def update_transaction_status(transaction_id: int) -> None:
    with SessionLocal() as db:
        transaction = db.query(Transaction).get(transaction_id)

        if transaction:
            transaction.status = TransactionStatus.AUTHORIZED
            db.commit()
            return

        print("No transaction found")
