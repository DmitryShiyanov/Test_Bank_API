import pytest

from src.main.api.generators.creation_rule import UserRole
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest



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
def user_with_two_accounts(api_manager, create_user_request):
    first_account = api_manager.user_steps.create_account(create_user_request)
    second_account = api_manager.user_steps.create_account(create_user_request)
    return first_account, second_account

@pytest.fixture
def user_credit_account(api_manager, create_credit_secret_user_request):
    return api_manager.user_steps.create_account(create_credit_secret_user_request)

@pytest.fixture
def user_with_two_credit_accounts(api_manager, create_credit_secret_user_request):
    first = api_manager.user_steps.create_account(create_credit_secret_user_request)
    second = api_manager.user_steps.create_account(create_credit_secret_user_request)
    return first, second
