from http import HTTPStatus

from pydantic_core.core_schema import ValidatorFunctionWrapHandler

from src.main.api.foundation.endpoint import EndPoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models import create_user_request
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.transactions_request import TransactionsRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.CREATE_ACCOUNT,
            ResponseSpecs.request_create()
        ).post()
        return response

    def create_account_failure(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.CREATE_ACCOUNT_FAILURE,
            ResponseSpecs.request_max_acc()
        ).post()
        return response

    def deposit(self, account_deposit_request: AccountDepositRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(account_deposit_request)
        return response

    def deposit_failure(self, account_deposit_request: AccountDepositRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.DEPOSIT_FAILURE,
            ResponseSpecs.request_bad()
        ).post(account_deposit_request)
        return response

    def transfer(self, account_transfer_request: AccountTransferRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(account_transfer_request)
        return response

    def transfer_failure(self, account_transfer_request: AccountTransferRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.Transfer_FAILURE,
            ResponseSpecs.request_bad()
        ).post(account_transfer_request)
        return response

    def credit_accept(self, credit_request: CreateCreditRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.CREDIT,
            ResponseSpecs.request_create()
        ).post(credit_request)
        return response

    def credit_failure(self, credit_request: CreateCreditRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.CREDIT_FAILURE,
            ResponseSpecs.has_status_any(
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.NOT_FOUND
            )
        ).post(credit_request)
        return response

    def credit_repay(self, credit_repay_request: CreditRepayRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def credit_repay_failure(self, credit_repay_request: CreditRepayRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.CREDIT_REPAY_FAILURE,
            ResponseSpecs.request_422_error()
        ).post(credit_repay_request)
        return response

    def account_transactions(self, transactions_request: TransactionsRequest, create_user_request: CreateUserRequest):
        id = transactions_request.id
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            EndPoint.TRANSACTION,
            ResponseSpecs.request_ok()
        ).get(id)
        return response