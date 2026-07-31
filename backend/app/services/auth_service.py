from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self):
        self.repository = UserRepository()

    def register(self, db: Session, payload: RegisterRequest):
        if self.repository.get_by_email(db, payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email đã được sử dụng')
        user = User(
            full_name=payload.full_name,
            email=payload.email.casefold(),
            password_hash=hash_password(payload.password),
            phone=payload.phone,
            role='CUSTOMER',
            is_active=True,
        )
        try:
            return self.repository.create(db, user)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email đã được sử dụng') from exc

    def login(self, db: Session, payload: LoginRequest):
        user = self.repository.get_by_email(db, payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email hoặc mật khẩu không chính xác',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Tài khoản đã bị khóa')
        return {
            'access_token': create_access_token(user.id),
            'token_type': 'bearer',
            'user': user,
        }
