from sqlalchemy import Column, Integer, ForeignKey, Float
from src.main.api.db.base import Base

class RepayTable(Base):
    __tablename__ = "repay"
    id = Column(Integer, primary_key=True, autoincrement=True)
    creditId = Column(Integer, ForeignKey('credit_table.id'), nullable=False)
    accountId = Column(Integer, ForeignKey('account.id'), nullable=False)
    amount = Column(Float, nullable=False)
    amountDeposited = Column (Float, nullable=False)

    def __repr__(self):
        return f"<Repay(id={self.id}, creditId={self.creditId}, accountId={self.accountId}, amount={self.amount}, amountDeposited={self.amountDeposited})>"