from src.main.api.models.base_model import BaseModel


class AccountTransferResponseError(BaseModel):
    error: str
