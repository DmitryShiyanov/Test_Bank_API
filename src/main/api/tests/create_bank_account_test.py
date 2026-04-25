import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateBankAccount:
    def test_account_creation(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, "Аккаунт не создан,  ID аккаунта нет в БД"
        assert account_from_db.balance is not None, "Поле баланса для аккаунта отсутствует в БД"

    def test_more_then_two_bank_account_creation(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        api_manager.user_steps.create_account(create_user_request)
        api_manager.user_steps.create_account(create_user_request)
        response_3 = api_manager.user_steps.create_account_failure(create_user_request)

        assert response_3.error == "User already has maximum number of accounts(2)"

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is not None, "Пользователь не найден в БД"

        account_from_db = Account.get_accounts_count_by_user_id(db_session, user_from_db.id)
        assert account_from_db == 2, "Создался 3-й аккаунт, ошибка"
