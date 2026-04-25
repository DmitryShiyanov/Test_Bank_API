from enum import Enum

from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.account_transer_response import AccountTransferResponse
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response_error import AccountTransferResponseError
from src.main.api.models.accunt_deposit_response_error import AccountDepositResponseError
from src.main.api.models.base_model import BaseModel
from typing import Optional, Type
from dataclasses import dataclass

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_account_response_error import CreateAccountResponseError
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_credit_response import CreateCreditResponse
from src.main.api.models.create_credit_response_error import CreateCreditResponseError
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_repay_response_error import CreditRepayResponseError
from src.main.api.models.get_all_users_response import AllUsersResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transactions_request import TransactionsRequest
from src.main.api.models.transactions_response import AccountResponse
from src.main.api.models.user_delete_request import DeleteUserRequest
from src.main.api.models.user_delete_response import DeleteUserResponse


@dataclass
class EndPointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class EndPoint(Enum):
    ADMIN_CREATE_USER = EndPointConfiguration(
        request_model = CreateUserRequest,
        url = "/admin/create",
        response_model = CreateUserResponse,
    )
    ADMIN_DELETE_USER = EndPointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = None
    )

    LOGIN_USER = EndPointConfiguration(
        request_model = LoginUserRequest,
        url = "/auth/token/login",
        response_model  = LoginUserResponse
    )

    CREATE_ACCOUNT = EndPointConfiguration(
        request_model = None,
        url="/account/create",
        response_model = CreateAccountResponse
    )
    CREATE_ACCOUNT_FAILURE = EndPointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model = CreateAccountResponseError
    )

    DEPOSIT = EndPointConfiguration(
        request_model = AccountDepositRequest,
        url = "/account/deposit",
        response_model=AccountDepositResponse
    )

    DEPOSIT_FAILURE = EndPointConfiguration(
        request_model = AccountDepositRequest,
        url = "/account/deposit",
        response_model = AccountDepositResponseError
    )

    TRANSFER = EndPointConfiguration(
        request_model = AccountTransferRequest,
        url = "/account/transfer",
        response_model = AccountTransferResponse
    )

    Transfer_FAILURE = EndPointConfiguration(
        request_model = AccountTransferRequest,
        url = "/account/transfer",
        response_model = AccountTransferResponseError
    )

    CREDIT = EndPointConfiguration(
        request_model = CreateCreditRequest,
        url = "/credit/request",
        response_model = CreateCreditResponse
    )
    CREDIT_FAILURE = EndPointConfiguration(
        request_model = CreateCreditRequest,
        url = "/credit/request",
        response_model = CreateCreditResponseError
    )
    CREDIT_REPAY = EndPointConfiguration(
        request_model = CreditRepayRequest,
        url = "/credit/repay",
        response_model = CreditRepayResponse
    )

    CREDIT_REPAY_FAILURE = EndPointConfiguration(
        request_model = CreditRepayRequest,
        url = "/credit/repay",
        response_model = CreditRepayResponseError
    )

    TRANSACTION = EndPointConfiguration(
        request_model = TransactionsRequest,
        url = "/account/transactions",
        response_model = AccountResponse
    )

    ALL_USERS = EndPointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = AllUsersResponse
    )