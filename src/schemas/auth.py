from pydantic import Field

from src.config import BaseSchema


class AuthSchema(BaseSchema):
    name: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=64)
