from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src import security
from src.database import db_dep
from src.models import User
from src.schemas.auth import AuthSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(auth_schema: AuthSchema, session: db_dep):
    request = select(User).where(User.name == auth_schema.name)
    user = (await session.execute(request)).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    hashed_password = security.hash_password(auth_schema.password)
    user = User(name=auth_schema.name, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return security.create_access_token(security.Payload(sub=str(user.id)))


@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: db_dep):
    request = select(User).where(User.name == form_data.username)
    user = (await session.execute(request)).scalar_one_or_none()
    if user is None or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this name and password not found")
    return security.create_access_token(security.Payload(sub=str(user.id)))
