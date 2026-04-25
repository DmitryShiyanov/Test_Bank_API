import requests

from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.accunt_deposit_response_error import AccountDepositResponseError
from src.main.api.requests.requester import Requester


class DepositRequester(Requester):
    def post(self, account_deposit_request: AccountDepositRequest) -> AccountDepositResponse | AccountDepositResponseError:
        url=f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=account_deposit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == 400:
            return AccountDepositResponseError(**response.json())
        return AccountDepositResponse(**response.json())