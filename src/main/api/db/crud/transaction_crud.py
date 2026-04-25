from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import TransactionTable


class TransactionCrudDb:
    @staticmethod
    def get_deposit_by_id(db: Session, id: int) -> TransactionTable | None:
        return db.query(TransactionTable).filter_by(from_account_id=id).first()
