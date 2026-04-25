from datetime import datetime
from typing import Optional, List

from src.main.api.models.base_model import BaseModel


class TransactionsResponse(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int] = None
    toAccountId: Optional[int] = None
    createdAt: datetime
    creditId: Optional[int] = None

class AccountResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[TransactionsResponse]