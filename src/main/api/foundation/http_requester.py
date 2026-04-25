
from typing import Callable, Dict
from src.main.api.foundation.endpoint import EndPoint


class HttpRequester:
    def __init__(self, request_spec: Dict, endpoint: EndPoint, response_spec: Callable):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec