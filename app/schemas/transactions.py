import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.transactions import TransactionType


class TransactionBase(BaseModel):
    type: TransactionType
    amount: Decimal = Field(..., gt=0)
    category: str = Field(default="lainnya", max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    transaction_date: Optional[datetime] = None


class TransactionCreateInput(TransactionBase):
    pass

class TransactionCreate(TransactionBase):
    telegram_user_id: int


class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    category: Optional[str] = None
    description: Optional[str] = None
    transaction_date: Optional[datetime] = None


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    telegram_user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class TransactionSummary(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None