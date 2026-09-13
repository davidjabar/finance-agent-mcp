import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Numeric, DateTime, Enum, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_user_id = Column(BigInteger, nullable=False, index=True)

    type = Column(Enum(TransactionType, name="transaction_type"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    category = Column(String(50), nullable=False, default="lainnya")
    description = Column(String(255), nullable=True)

    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Transaction {self.type} {self.amount} - {self.category}>"