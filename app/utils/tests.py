from typing import Any


class MockResponse:
    def __init__(self, json_data: dict[Any, Any], status_code: int):
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> dict[Any, Any]:
        return self.json_data
