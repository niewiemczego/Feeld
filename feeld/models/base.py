from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class InnerResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class BaseResponse(ABC, InnerResponse):
    @classmethod
    @abstractmethod
    def parse_response(cls, data: dict[str, Any]) -> "BaseResponse | None": ...
