from sqlalchemy.orm import Session
from typing import List

from ..models.user import User

async def add_user(user: User, db: Session) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_user(user_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    return user


def soft_delete(user_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .where(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    if user:
        user.is_deleted = True
        db.commit()
        db.refresh(user)
        return user
    return None


def search_user(name: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.name == name and User.is_deleted == False)
        .first()
    )
    return user


async def all_users(db: Session) -> List[User]:
    db_users = db.query(User).filter(User.is_deleted == False).all()
    return db_users


def search_user_id(user_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    return user


def update_password(user_id: str, new_password: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    if not user:
        return None
    user.password = new_password
    db.commit()
    db.refresh(user)
    return user


def update_playlist(user_id: str, new_playlist_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    if not user:
        return None
    user.playlist_id = new_playlist_id
    db.commit()
    db.refresh(user)
    return user


async def search_users_by_name(name: str, db: Session):
    db_users = db.query(User).filter(User.is_deleted == False).all()
    filtered_users = [user for user in db_users if name in user.name.lower()]
    return filtered_users
