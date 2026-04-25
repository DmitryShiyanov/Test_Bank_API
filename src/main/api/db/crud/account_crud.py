from sqlalchemy.orm import Session
from src.main.api.db.models.account_table import Account


class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db_session: Session, account_id: int) -> Account | None:
        return db_session.query(Account).filter_by(id=account_id).first()

    @staticmethod
    def get_accounts_count_by_user_id(db_session: Session, user_id: int) -> int:
        return db_session.query(Account).filter_by(user_id=user_id).count()

    @staticmethod
    def delete_account(db_session: Session, account_id: int) -> None:
        account = db_session.query(Account).filter_by(id=account_id).first()
        if account:
            db_session.delete(account)
            db_session.commit()