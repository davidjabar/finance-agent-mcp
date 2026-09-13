import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transactions import Transaction, TransactionType
from app.schemas.transactions import TransactionCreate, TransactionUpdate
from app.utils.datetime import to_naive


def create_transaction(db: Session, data: TransactionCreate) -> Transaction:
    tx = Transaction(**data.model_dump(exclude_none=True))
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def get_transaction(db: Session, tx_id: uuid.UUID) -> Optional[Transaction]:
    return (
        db.query(Transaction)
        .filter(Transaction.id == tx_id, Transaction.deleted_at.is_(None))
        .first()
    )


def list_transactions(db: Session,telegram_user_id: int,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      limit: int = 50,
                      offset: int = 0,) -> Sequence[Transaction]:

    start_date = to_naive(start_date)
    end_date = to_naive(end_date)
    q = db.query(Transaction).filter(
        Transaction.telegram_user_id == telegram_user_id,
        Transaction.deleted_at.is_(None),
    )
    if start_date:
        q = q.filter(Transaction.transaction_date >= start_date)
    if end_date:
        q = q.filter(Transaction.transaction_date <= end_date)
    return q.order_by(Transaction.transaction_date.desc()).offset(offset).limit(limit).all()


def update_transaction(db: Session, tx_id: uuid.UUID, data: TransactionUpdate) -> Optional[Transaction]:
    tx = get_transaction(db, tx_id)
    if not tx:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(tx, field, value)
    db.commit()
    db.refresh(tx)
    return tx


def delete_transaction(db: Session, tx_id: uuid.UUID) -> bool:
    """Soft delete — row tetap ada di DB, cuma ditandai deleted_at."""
    tx = get_transaction(db, tx_id)
    if not tx:
        return False
    tx.deleted_at = datetime.utcnow()
    db.commit()
    return True


def restore_transaction(db: Session, tx_id: uuid.UUID) -> Optional[Transaction]:
    """Optional helper buat un-delete kalau ternyata salah hapus."""
    tx = (
        db.query(Transaction)
        .filter(Transaction.id == tx_id, Transaction.deleted_at.isnot(None))
        .first()
    )
    if not tx:
        return None
    tx.deleted_at = None
    db.commit()
    db.refresh(tx)
    return tx


def get_summary(db: Session,telegram_user_id: int,
                start_date: Optional[datetime] = None,
                end_date: Optional[datetime] = None,) -> dict:
    
    start_date = to_naive(start_date)
    end_date = to_naive(end_date)
    q = db.query(Transaction).filter(
        Transaction.telegram_user_id == telegram_user_id,
        Transaction.deleted_at.is_(None),
    )
    if start_date:
        q = q.filter(Transaction.transaction_date >= start_date)
    if end_date:
        q = q.filter(Transaction.transaction_date <= end_date)

    income = q.filter(Transaction.type == TransactionType.INCOME).with_entities(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).scalar()
    expense = q.filter(Transaction.type == TransactionType.EXPENSE).with_entities(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).scalar()

    income, expense = Decimal(income), Decimal(expense)

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
        "period_start": start_date,
        "period_end": end_date,
    }