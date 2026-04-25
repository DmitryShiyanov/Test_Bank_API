
from typing import List
import requests

from src.main.api.models.get_all_users_response import AllUsersResponse
from src.main.api.requests.requester import Requester


class GetAllUsersRequester(Requester):
    def post(self, model=None) -> List[AllUsersResponse]:
        url=f"{self.base_url}/admin/users"
        response = requests.get(
            url=url,
            headers=self.headers,
        )
        self.response_spec(response)
        return [AllUsersResponse(**user) for user in response.json()]