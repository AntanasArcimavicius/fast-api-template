import enum

from sqlalchemy import DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TransactionStatus(enum.Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    DECLINED = "declined"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_number: Mapped[str] = mapped_column(String)
    expiry: Mapped[DateTime] = mapped_column(DateTime)
    amount: Mapped[float] = mapped_column(Numeric)
    merchant_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), default=TransactionStatus.PENDING
    )
