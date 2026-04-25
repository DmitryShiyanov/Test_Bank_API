import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit



@pytest.mark.api
class TestCredit:
    @pytest.mark.parametrize("amount", [5000.0, 15000.0])
    def test_credit_create_valid(self, db_session: Session, api_manager: ApiManager, create_credit_secret_user_request: CreateUserRequest, amount: int):
        response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        credit_request = CreateCreditRequest(accountId=response.id, amount=amount, termMonths=12)
        credit_response = api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)

        assert credit_response.balance == amount
        assert credit_response.termMonths == 12

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.id)
        assert credit_from_db is not None
        assert credit_from_db.amount == amount
        assert credit_from_db.term_months == 12
        assert credit_from_db.balance == -amount



    @pytest.mark.parametrize("amount", [4999, 15001.1])
    def test_credit_create_invalid(self, db_session: Session, api_manager: ApiManager, create_credit_secret_user_request: CreateUserRequest, amount: int):
        response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        credit_request = CreateCreditRequest(accountId=response.id, amount=amount, termMonths=12)
        credit_response = api_manager.user_steps.credit_failure(credit_request, create_credit_secret_user_request)

        assert credit_response.error == "Amount must be between 5000 and 15000"

        credit_from_db = Credit.get_credit_by_id(db_session, credit_request.accountId)
        print(credit_from_db)
        assert credit_from_db is None, "Кредит успешно оформлен"


    def test_credit_repay_success(self, db_session: Session, api_manager: ApiManager, create_credit_secret_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        credit_request = CreateCreditRequest(accountId=response.id, amount=5000, termMonths=12)
        credit_response = api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)

        repay_request = CreditRepayRequest(creditId=credit_response.creditId, accountId=credit_response.id,amount=5000)
        response_repay = api_manager.user_steps.credit_repay(repay_request, create_credit_secret_user_request)

        assert response_repay.amountDeposited == 5000

        credit_repay_from_db = Credit.get_credit_by_id(db_session, credit_response.id)
        assert credit_repay_from_db is not None
        assert credit_repay_from_db.amount == 5000
        assert credit_repay_from_db.balance == 0, "Кредит не погашен"


    @pytest.mark.parametrize("credit_amount, repay_amount", [(10000, 5000)])
    def test_credit_repay_failure(self, db_session: Session, api_manager: ApiManager, create_credit_secret_user_request: CreateUserRequest, credit_amount: int, repay_amount: int):
        response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        credit_request = CreateCreditRequest(accountId=response.id, amount=credit_amount, termMonths=12)
        credit_response = api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)

        repay_request = CreditRepayRequest(creditId=credit_response.creditId, accountId=credit_response.id, amount=repay_amount)
        response_repay = api_manager.user_steps.credit_repay_failure(repay_request, create_credit_secret_user_request)

        assert response_repay.error == f"The amount is not enough. Credit balance: -{credit_amount}"
        credit_repay_from_db = Credit.get_credit_by_id(db_session, credit_response.id)
        assert credit_repay_from_db is not None
        assert credit_repay_from_db.amount == credit_amount
        assert credit_repay_from_db.balance == -credit_amount



    def test_credit_create_twice_failure(self, db_session: Session, api_manager: ApiManager, create_credit_secret_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        credit_request = CreateCreditRequest(accountId=response.id, amount=5000, termMonths=12)
        api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)
        credit_request_2 = CreateCreditRequest(accountId=response.id, amount=5000, termMonths=12)
        response_failure = api_manager.user_steps.credit_failure(credit_request_2, create_credit_secret_user_request)

        assert response_failure.error == "Only one active credit allowed per user"

        credit_from_db = Credit.get_credit_user_count(db_session, response.id)
        print(credit_from_db)
        assert credit_from_db is not None
        assert credit_from_db == 1, "Создали второй кредит"

    def test_credit_create_on_second_credit_id_failure(self, db_session: Session, api_manager: ApiManager, create_credit_secret_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_credit_secret_user_request)
        response2 = api_manager.user_steps.create_account(create_credit_secret_user_request)

        credit_request = CreateCreditRequest(accountId=response.id, amount=5000, termMonths=12)
        api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)

        credit_request_2 = CreateCreditRequest(accountId=response2.id, amount=5000, termMonths=12)
        response_failure = api_manager.user_steps.credit_failure(credit_request_2, create_credit_secret_user_request)

        assert response_failure.error == "Only one active credit allowed per user"

        credit_from_db = Credit.get_credit_user_count(db_session, response.id)
        credit_from_db_2 = Credit.get_credit_user_count(db_session, response2.id)
        assert credit_from_db is not None
        assert credit_from_db == 1, "Создали второй кредит"
        assert credit_from_db_2 == 0, "Создали кредит на другой аккаунт ID"
