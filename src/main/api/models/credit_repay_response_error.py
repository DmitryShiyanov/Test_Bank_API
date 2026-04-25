from src.main.api.models.base_model import BaseModel


class CreditRepayResponseError(BaseModel):
    error: str
