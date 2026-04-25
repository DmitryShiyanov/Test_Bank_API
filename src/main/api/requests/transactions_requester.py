import requests

from src.main.api.models.transactions_request import TransactionsRequest
from src.main.api.models.transactions_response import AccountResponse
from src.main.api.requests.requester import Requester


class TransactionRequester(Requester):
    def post(self, transactions_request: TransactionsRequest) -> AccountResponse:
        transaction = transactions_request.id
        url=f"{self.base_url}/account/transactions/{transaction}"
        response = requests.get(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        print("\nRESPONSE:", response.json())
        return AccountResponse(**response.json())