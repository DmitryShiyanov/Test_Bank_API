import pytest

from src.main.api.generators.creation_rule import UserRole
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.transactions_request import TransactionsRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(
        CreateUserRequest,
        overrides={"role": UserRole.USER}
    )
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_secret_user_request(api_manager):
    user_request = RandomModelGenerator.generate(
        CreateUserRequest,
        overrides={"role": UserRole.CREDIT_ROLE}
    )
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_another_user_request(api_manager):
    user_request = RandomModelGenerator.generate(
        CreateUserRequest,
        overrides={"role": UserRole.USER}
    )
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def user_account(api_manager, create_user_request):
    response = api_manager.user_steps.create_account(create_user_request)
    return response

@pytest.fixture
def user_account_and_request_fabric(create_user_request, user_account):
    def deposit_request(amount: int):
        request = AccountDepositRequest(accountId=user_account.id, amount=amount)
        return request
    return deposit_request

@pytest.fixture
def create_and_deposit_account(api_manager, create_user_request, user_account):
    deposit = AccountDepositRequest(accountId=user_account.id, amount=5000)
    deposit_apply = api_manager.user_steps.deposit(deposit, create_user_request)
    transaction_request = TransactionsRequest(id=deposit_apply.id)
    return deposit_apply, transaction_request


@pytest.fixture
def user_with_two_accounts(api_manager, create_user_request):
    first_account = api_manager.user_steps.create_account(create_user_request)
    second_account = api_manager.user_steps.create_account(create_user_request)
    return first_account, second_account

@pytest.fixture
def create_and_deposit_twice(api_manager, create_user_request, user_with_two_accounts):
    first, second = user_with_two_accounts
    account_deposit = AccountDepositRequest(accountId=first.id, amount=1000)
    api_manager.user_steps.deposit(account_deposit, create_user_request)
    account_deposit_2 = AccountDepositRequest(accountId=first.id, amount=9000)
    api_manager.user_steps.deposit(account_deposit_2, create_user_request)
    return first, second

@pytest.fixture
def deposit_factory(create_and_deposit_twice):
    first, second = create_and_deposit_twice
    def transfer_request(amount: int):
        request = AccountTransferRequest(fromAccountId=first.id, toAccountId=second.id, amount=amount)
        return first, second, request
    return transfer_request


@pytest.fixture
def user_credit_account(api_manager, create_credit_secret_user_request):
    return api_manager.user_steps.create_account(create_credit_secret_user_request)

@pytest.fixture
def user_with_two_credit_accounts(api_manager, create_credit_secret_user_request):
    first = api_manager.user_steps.create_account(create_credit_secret_user_request)
    second = api_manager.user_steps.create_account(create_credit_secret_user_request)
    credit_request = CreateCreditRequest(accountId=first.id, amount=5000, termMonths=12)
    api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)
    request = CreateCreditRequest(accountId=second.id, amount=5000, termMonths=12)
    return first, second, request

@pytest.fixture
def credit_factory(api_manager, user_credit_account):
    def credit_request(amount: int):
        request = CreateCreditRequest(accountId=user_credit_account.id,
                                      amount=amount,
                                      termMonths=12)
        return request
    return credit_request


@pytest.fixture
def credit_repay_factory(api_manager, user_credit_account, create_credit_secret_user_request):
    def credit_repay_request(amount: int):
        credit_request = CreateCreditRequest(
        accountId=user_credit_account.id,
        amount=amount,
        termMonths=12)
        response = api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)
        repay_request = CreditRepayRequest(creditId=response.creditId, accountId=response.id, amount=amount)
        return repay_request, response
    return credit_repay_request


@pytest.fixture
def credit_repay_factory_invalid(api_manager, user_credit_account, create_credit_secret_user_request):
    def credit_repay_request(amount1: int, amount2: int):
        credit_request = CreateCreditRequest(
        accountId=user_credit_account.id,
        amount=amount1,
        termMonths=12)
        response = api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)
        repay_request = CreditRepayRequest(creditId=response.creditId, accountId=response.id, amount=amount2)
        return repay_request, response
    return credit_repay_request


@pytest.fixture
def create_credit_twice_failure(api_manager, user_credit_account, create_credit_secret_user_request):
    credit_request = CreateCreditRequest(
    accountId=user_credit_account.id,
    amount=5000,
    termMonths=12)
    api_manager.user_steps.credit_accept(credit_request, create_credit_secret_user_request)
    request = CreateCreditRequest(accountId=user_credit_account.id, amount=5000, termMonths=12)
    return request