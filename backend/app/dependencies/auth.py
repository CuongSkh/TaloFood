from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
repository = UserRepository()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Thông tin xác thực không hợp lệ hoặc đã hết hạn',
    headers={'WWW-Authenticate': 'Bearer'},
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        subject = payload.get('sub')
        user_id = int(subject)
    except (ValueError, TypeError):
        raise credentials_exception
    user = repository.get(db, user_id)
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Tài khoản đã bị khóa')
    return current_user


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != 'ADMIN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Bạn không có quyền thực hiện thao tác này')
    return current_user
