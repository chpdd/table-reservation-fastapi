from src.config import BaseSchema


class CreateLocationSchema(BaseSchema):
    name: str


class LocationSchema(CreateLocationSchema):
    id: int
