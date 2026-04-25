from src.main.api.models.base_model import BaseModel


class AllUsersResponse(BaseModel):
    id: int
    username: str
    role: str