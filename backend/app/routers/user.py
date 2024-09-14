from typing import Annotated
from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.schemas import user as user_schemas
from app.utils.auth import authenticate_user
from app.utils.jwt import create_access_token
from app.dependencies import get_db_session


router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user_account(
    user_create: user_schemas.UserCreate,
    db: Session = Depends(get_db_session)
    ) -> user_schemas.UserOut:
    return crud_user.create_user(db=db, user=user_create)


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db_session)
    ):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return user_schemas.Token(access_token=access_token)
