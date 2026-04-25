from src.main.api.models.base_model import BaseModel


class CreateCreditResponseError(BaseModel):
    error: str
