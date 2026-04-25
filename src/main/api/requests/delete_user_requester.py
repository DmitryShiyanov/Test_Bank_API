import requests

from src.main.api.models.user_delete_request import DeleteUserRequest
from src.main.api.models.user_delete_response import DeleteUserResponse
from src.main.api.requests.requester import Requester


class DeleteUserRequester(Requester):
    def post(self, delete_user_request: DeleteUserRequest) -> DeleteUserResponse:
        user_id = delete_user_request.id
        url=f"{self.base_url}/admin/users/{user_id}"
        response = requests.delete(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        return DeleteUserResponse(**response.json())