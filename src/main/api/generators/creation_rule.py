from dataclasses import dataclass
from enum import Enum


@dataclass
class CreationRule:
    regex: str

class UserRole(str, Enum):
    ADMIN = "ROLE_ADMIN"
    USER = "ROLE_USER"
    CREDIT_ROLE = "ROLE_CREDIT_SECRET"