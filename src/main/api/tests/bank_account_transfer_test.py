import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.user_crud import UserCrudDb as User



@pytest.mark.api
class TestBankAccountTransfer:
    @pytest.mark.parametrize("transfer_amount, balance_amount", [
        (500, 9500),
        (10000, 0)
    ])
    def test_bank_acc_transfer_valid_one_user(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, transfer_amount: int, balance_amount: int, create_and_deposit_twice, deposit_factory):
        first_acc, second_acc, account_transfer_request = deposit_factory(transfer_amount)

        transfer_response = api_manager.user_steps.transfer(account_transfer_request, create_user_request)
        assert transfer_response.fromAccountIdBalance == balance_amount

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is not None, "Пользователь не найден в БД"

        account_from_db = Account.get_accounts_count_by_user_id(db_session, user_from_db.id)
        assert account_from_db == 2

        transaction_from_db = Transaction.get_deposit_by_id(db_session, transfer_response.fromAccountId)
        print(transaction_from_db)
        assert transaction_from_db is not None
        assert transaction_from_db.amount == transfer_amount, "Некорретная сумма"
        assert transaction_from_db.transaction_type == "transfer", "Неверный тип транзакции"
        assert transaction_from_db.from_account_id == first_acc.id, "Странный ID from_ID"
        assert transaction_from_db.to_account_id == second_acc.id, "Странный ID to_ID"


    @pytest.mark.parametrize("transfer_amount", [
        499, 10001
    ])
    def test_bank_acc_transfer_invalid_amount(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, transfer_amount: int, deposit_factory):
        first_acc, second_acc, account_transfer_request = deposit_factory(transfer_amount)

        transfer_response = api_manager.user_steps.transfer_failure(account_transfer_request, create_user_request)
        assert transfer_response.error == "Amount must be between 500 and 10000"

        account_from_db = Transaction.get_deposit_by_id(db_session, first_acc.id)
        assert account_from_db is None, "Баланс пополнен "
        assert first_acc.balance == 0


    """Создаем двух юзеров, создаем каждому по счету, пополняем А счет, переводим на Б счет"""
    def test_transfer_between_two_accounts(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_another_user_request: CreateUserRequest, deposit_factory):
        first_acc, second_acc, account_transfer_request = deposit_factory(5000)

        transfer_response = api_manager.user_steps.transfer(account_transfer_request, create_user_request)

        assert transfer_response.fromAccountIdBalance == 5000

        account_from_db = Transaction.get_deposit_by_id(db_session, first_acc.id)

        assert account_from_db is not None
        assert account_from_db.amount == 5000
        assert account_from_db.transaction_type == "transfer"
        assert account_from_db.from_account_id == first_acc.id
        assert account_from_db.to_account_id == second_acc.id
