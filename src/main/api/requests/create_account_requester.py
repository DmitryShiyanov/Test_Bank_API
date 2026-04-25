import requests

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_account_response_error import CreateAccountResponseError
from src.main.api.requests.requester import Requester


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse | CreateAccountResponseError:
        url=f"{self.base_url}/account/create"
        response= requests.post(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [409, 500, 403]:
            return CreateAccountResponseError(**response.json())
        return CreateAccountResponse(**response.json())
