import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transactions_request import TransactionsRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction



@pytest.mark.api
class TestBankAccountTransactions:
    def test_account_transactions(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):

        response = api_manager.user_steps.create_account(create_user_request)

        account_deposit = AccountDepositRequest(accountId=response.id, amount=5000)
        deposit_apply = api_manager.user_steps.deposit(account_deposit, create_user_request)

        transaction_request = TransactionsRequest(id=deposit_apply.id)
        response_transaction = api_manager.user_steps.account_transactions(transaction_request, create_user_request)

        assert response_transaction.transactions[0].type == "deposit"
        assert response_transaction.transactions[0].toAccountId == response.id

        transaction_from_db = Transaction.get_deposit_by_id(db_session, response_transaction.transactions[0].fromAccountId)
        assert transaction_from_db is not None, "Не было транзакций"
        assert transaction_from_db.transaction_type == "deposit", "Пустое поле"
