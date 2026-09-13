import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.schemas.transactions import (
    TransactionCreate,
    TransactionCreateInput,
    TransactionRead,
    TransactionUpdate,
    TransactionSummary,
)
from app.services import transactions

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_current_telegram_user_id() -> int:
    """Single-user app, jadi user id-nya fixed dari config."""
    return settings.OWNER_TELEGRAM_ID


@router.post(
    "",
    response_model=TransactionRead,
    status_code=201,
    operation_id="add_transaction",
    summary="Catat transaksi baru",
)
def create_transaction(
    payload: TransactionCreateInput,
    telegram_user_id: int = Depends(get_current_telegram_user_id),
    db: Session = Depends(get_db),
):
    data = TransactionCreate(**payload.model_dump(), telegram_user_id=telegram_user_id)
    return transactions.create_transaction(db, data)


@router.get("", response_model=List[TransactionRead], operation_id="list_transactions")
def list_transactions(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    telegram_user_id: int = Depends(get_current_telegram_user_id),
    db: Session = Depends(get_db),
):
    return transactions.list_transactions(db, telegram_user_id, start_date, end_date, limit, offset)


@router.get("/summary", response_model=TransactionSummary, operation_id="get_transaction_summary")
def summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    telegram_user_id: int = Depends(get_current_telegram_user_id),
    db: Session = Depends(get_db),
):
    return transactions.get_summary(db, telegram_user_id, start_date, end_date)


@router.get("/{tx_id}", response_model=TransactionRead, operation_id="get_transaction")
def get_transaction(tx_id: uuid.UUID, db: Session = Depends(get_db)):
    tx = transactions.get_transaction(db, tx_id)
    if not tx:
        raise HTTPException(404, "Transaction not found")
    return tx


@router.patch("/{tx_id}", response_model=TransactionRead, operation_id="update_transaction")
def update_transaction(tx_id: uuid.UUID, payload: TransactionUpdate, db: Session = Depends(get_db)):
    tx = transactions.update_transaction(db, tx_id, payload)
    if not tx:
        raise HTTPException(404, "Transaction not found")
    return tx


@router.delete("/{tx_id}", status_code=204, operation_id="delete_transaction")
def delete_transaction(tx_id: uuid.UUID, db: Session = Depends(get_db)):
    if not transactions.delete_transaction(db, tx_id):
        raise HTTPException(404, "Transaction not found")