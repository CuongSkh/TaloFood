import math
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRoleUpdate, UserStatusUpdate, UserUpdateProfile


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create(self, db: Session, payload: UserCreate):
        if self.repository.get_by_email(db, payload.email):
            raise HTTPException(status_code=409, detail='Email đã tồn tại')
        user = User(full_name=payload.full_name, email=payload.email.casefold(), password_hash=hash_password(payload.password),
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

    def update_profile(self, db: Session, user: User, payload: UserUpdateProfile):
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(user, field, value)
        return self.repository.update(db, user)

    def update_status(self, db: Session, target_id: int, payload: UserStatusUpdate, current_admin: User):
        target = self.get(db, target_id)
        if target.id == current_admin.id and not payload.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Admin không thể tự khóa tài khoản của mình')
        target.is_active = payload.is_active
        return self.repository.update(db, target)

    def update_role(self, db: Session, target_id: int, payload: UserRoleUpdate, current_admin: User):
        target = self.get(db, target_id)
        if target.id == current_admin.id and payload.role != 'ADMIN':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Admin không thể tự hạ quyền của mình')
        target.role = payload.role
        return self.repository.update(db, target)
