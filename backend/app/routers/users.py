from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_active_user, require_admin
from app.models.user import User
from app.schemas.user import (
    PaginatedUserResponse,
    UserCreate,
    UserResponse,
    UserRoleUpdate,
    UserStatusUpdate,
    UserUpdateProfile,
)
from app.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['Users'])
service = UserService()


@router.get('/me', response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.patch('/me', response_model=UserResponse)
def update_my_profile(payload: UserUpdateProfile, current_user: User = Depends(get_current_active_user),
                      db: Session = Depends(get_db)):
    return service.update_profile(db, current_user, payload)


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return service.create(db, payload)


@router.get('', response_model=PaginatedUserResponse)
def list_users(page: int = Query(default=1, ge=1), size: int = Query(default=20, ge=1, le=100),
               db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return service.list(db, page, size)


@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return service.get(db, user_id)


@router.patch('/{user_id}/status', response_model=UserResponse)
def update_user_status(user_id: int, payload: UserStatusUpdate, db: Session = Depends(get_db),
                       current_admin: User = Depends(require_admin)):
    return service.update_status(db, user_id, payload, current_admin)


@router.patch('/{user_id}/role', response_model=UserResponse)
def update_user_role(user_id: int, payload: UserRoleUpdate, db: Session = Depends(get_db),
                     current_admin: User = Depends(require_admin)):
    return service.update_role(db, user_id, payload, current_admin)
