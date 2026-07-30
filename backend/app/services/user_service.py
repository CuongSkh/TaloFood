import math
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create(self, db: Session, payload: UserCreate):
        if self.repository.get_by_email(db, payload.email):
            raise HTTPException(status_code=409, detail='Email đã tồn tại')
        user = User(full_name=payload.full_name, email=payload.email, password_hash=hash_password(payload.password),
                    phone=payload.phone, role=payload.role, is_active=payload.is_active)
        try:
            return self.repository.create(db, user)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=409, detail='Email đã tồn tại') from exc

    def list(self, db: Session, page: int, size: int):
        items, total = self.repository.list(db, page, size)
        return {'items': items, 'total': total, 'page': page, 'size': size,
                'totalPages': math.ceil(total / size) if total else 0}

    def get(self, db: Session, user_id: int):
        user = self.repository.get(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail='Không tìm thấy người dùng')
        return user
