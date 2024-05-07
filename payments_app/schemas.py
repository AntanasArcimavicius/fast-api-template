from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator

from payments_app.models import TransactionStatus

CREDIT_CARD_REGEX = "(^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)"


class TransactionBase(BaseModel):
    expiry: datetime
    merchant_id: int
    card_number: str = Field(..., pattern=CREDIT_CARD_REGEX)
    amount: float = Field(
        ..., gt=0, description="The amount must be greater than zero."
    )

    @field_validator("card_number")
    def validate_card_number(cls, number: str):
        if len(number) != 16:
            raise ValueError("Card number is not valid")
        return number

    @field_validator("expiry")
    def validate_expiry(cls, date: datetime):
        if date.astimezone(timezone.utc) < datetime.now(timezone.utc):
            raise ValueError("Expiry date cannot be in the past")
        return date


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    status: TransactionStatus = TransactionStatus.PENDING

    class Config:
        from_attributes = True


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None
