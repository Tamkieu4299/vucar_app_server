from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from ..models.user import User
from ..models.authority import Authority
from ..utils.hash import hash_password
import uuid


def seed_data():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Authority).count() != 3:
            auth_data = [
                {
                    "authority_id": 0,
                    "name": "admin",
                    "inspect": True,
                    "view": True,
                    "user_edit": True,
                },
                {
                    "authority_id": 1,
                    "name": "mechanical",
                    "inspect": True,
                    "view": True,
                    "user_edit": False,
                },
                {
                    "authority_id": 2,
                    "name": "viewer",
                    "inspect": False,
                    "view": True,
                    "user_edit": False,
                },
            ]
            for data in auth_data:
                auth = Authority(**data)
                db.add(auth)
            db.commit()

        if not db.query(User).count():
            user_data = [
                {
                    "name": "admin",
                    "password": hash_password("123456"),
                    "authority_id": 0,
                },
                {
                    "name": "mechanical",
                    "password": hash_password("123456"),
                    "authority_id": 1,
                },
                {
                    "name": "viewer",
                    "password": hash_password("123456"),
                    "authority_id": 2,
                },
            ]
            for data in user_data:
                user = User(**data)
                db.add(user)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
