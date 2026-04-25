import requests

from src.main.api.models.create_credit_response import CreateCreditResponse
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_credit_response_error import CreateCreditResponseError
from src.main.api.requests.requester import Requester


class CreateCreditRequester(Requester):
    def post(self, create_credit_request: CreateCreditRequest) -> CreateCreditResponse | CreateCreditResponseError:
        url=f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=create_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [400, 403, 404]:
            return CreateCreditResponseError(**response.json())
        return CreateCreditResponse(**response.json())