from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.utils.hashing import verify_password


def authenticate_user(db: Session, username: str, password: str):
    user = user_crud.get_user_by_username(
        db=db,
        username=username
    )
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
