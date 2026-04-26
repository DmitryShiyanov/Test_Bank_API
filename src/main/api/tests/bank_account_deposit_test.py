import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account



@pytest.mark.api
class TestBankAccountDeposit:
    @pytest.mark.parametrize("amount", [1000, 5000, 9000])
    def test_account_deposit_with_valid_amount(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int, user_account: CreateUserRequest):
        account_deposit = AccountDepositRequest(accountId=user_account.id, amount=amount)
        deposit_apply = api_manager.user_steps.deposit(account_deposit, create_user_request)

        assert deposit_apply.balance == amount

        account_from_db = Account.get_account_by_id(db_session, deposit_apply.id)
        assert account_from_db is not None, "Аккаунт не найден в БД"
        print(account_from_db)
        assert account_from_db.balance == amount, "Сумма транзакции в БД неверная"


    @pytest.mark.parametrize("amount", [999,9001])
    def test_account_deposit_with_invalid_amount(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int, user_account: CreateUserRequest):
        account_before = Account.get_account_by_id(db_session, user_account.id)
        assert account_before.balance == 0, "Начальный баланс аккаунта должен быть 0"

        account_deposit = AccountDepositRequest(accountId=user_account.id, amount=amount)
        deposit_apply = api_manager.user_steps.deposit_failure(account_deposit, create_user_request)

        assert deposit_apply.error == "Amount must be between 1000 and 9000"

        account_after = Account.get_account_by_id(db_session, user_account.id)
        assert account_after.balance == 0, f"Баланс аккаунта изменился на {amount}"
