from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_username
from app.database import SessionLocal
from app.models import User as UserModel
from app.utils.jwt import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token=token)
    if not token_data:
        raise credentials_exception
    user = get_user_by_username(db=db, username=token_data.username)
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(
        user: UserModel = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user
