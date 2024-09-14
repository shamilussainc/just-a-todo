from sqlalchemy.orm import Session
from app.schemas import user as user_schemas
from app.models import User as UserModel
from app.utils.hashing import get_password_hash


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    return db.query(UserModel).where(UserModel.username == username).first()


def create_user(
        db: Session,
        user: user_schemas.UserCreate,
         ):
    user_in_db = UserModel()
    user_in_db.username = user.username
    user_in_db.email = user.email
    user_in_db.hashed_password = get_password_hash(user.password.get_secret_value())
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)

    return user_in_db
