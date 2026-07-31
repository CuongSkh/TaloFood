from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def get_by_email(self, db: Session, email: str):
        return db.scalar(select(User).where(func.lower(User.email) == email.casefold()))

    def get(self, db: Session, user_id: int):
        return db.get(User, user_id)

    def list(self, db: Session, page: int, size: int):
        total = db.scalar(select(func.count(User.id))) or 0
        items = db.scalars(select(User).order_by(User.id).offset((page - 1) * size).limit(size)).all()
        return list(items), total

    def create(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
