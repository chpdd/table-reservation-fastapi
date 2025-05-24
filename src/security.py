import datetime as dt
from typing import Annotated

import fastapi.security
import jwt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import Field

from src.config import BaseSchema, settings
from src.database import db_dep
from src.models import User

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Header(BaseSchema):
    alg: str = settings.JWT_ALGORITHM
    typ: str = "JWT"


class Payload(BaseSchema):
    sub: str | None = Field(default=None)
    exp: dt.datetime | None = Field(default=None)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: Payload | dict, expires_delta_minutes: int | None = 30):
    match data:
        case Payload(sub=None, exp=None) | {}:
            sub = "None"
            exp = dt.datetime.now() + dt.timedelta(minutes=expires_delta_minutes)
        case Payload(sub=sub, exp=None) | {"sub": sub}:
            exp = dt.datetime.now() + dt.timedelta(minutes=expires_delta_minutes)
        case Payload(sub=sub, exp=exp) | {"sub": sub, "exp": exp}:
            ...
        case _:
            raise TypeError("Payload must be of type dict or Payload")
    payload = Payload(sub=sub, exp=exp)
    access_token = jwt.encode(payload=payload.model_dump(), key=settings.JWT_SECRET_KEY,
                              algorithm=settings.JWT_ALGORITHM)
    result = {"access_token": access_token, "token_type": "bearer"}
    return result


def decode_access_token(token):
    return jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)


def only_authenticated(token: Annotated[str, Depends(oauth2_scheme)]):
    return True


def get_payload(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = Payload(**decode_access_token(token))
    return payload


def get_actual_user_id(payload: Annotated[Payload, Depends(get_payload)]):
    return int(payload.sub)


async def only_admin(user_id: Annotated[int, Depends(get_actual_user_id)], session: db_dep):
    user = await session.get(User, user_id)
    if user.is_admin:
        return user_id
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access forbidden. This route is available only for admins.")


only_authenticated_dep = Annotated[bool, Depends(only_authenticated)]
payload_dep = Annotated[Payload, Depends(get_payload)]
actual_user_id_dep = Annotated[int, Depends(get_actual_user_id)]
only_admin_dep = Annotated[int, Depends(only_admin)]
