import datetime
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from src.main.api.db.base import Base

class CreditTable(Base):
    __tablename__ = "credit"
    id = Column(Integer, primary_key=True,autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.id"),nullable=False)
    amount = Column(Float, nullable=False)
    term_months = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"Credit(id={self.id}, amount={self.amount}, account_id={self.account_id}, term_months={self.term_months}, balance={self.balance}, created_at={self.created_at})"
