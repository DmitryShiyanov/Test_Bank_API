import requests

from src.main.api.models.account_transer_response import AccountTransferResponse
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response_error import AccountTransferResponseError
from src.main.api.requests.requester import Requester


class TransferRequester(Requester):
    def post(self, account_transfer_request: AccountTransferRequest) -> AccountTransferResponse | AccountTransferResponseError:
        url=f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=account_transfer_request.model_dump(),
            headers=self.headers
        )
        if response.status_code == 400:
            return AccountTransferResponseError(**response.json())
        return AccountTransferResponse(**response.json())
