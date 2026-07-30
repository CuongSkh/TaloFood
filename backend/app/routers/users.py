from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import PaginatedUserResponse, UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['Users'])
service = UserService()

@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return service.create(db, payload)

@router.get('', response_model=PaginatedUserResponse)
def list_users(page: int = Query(default=1, ge=1), size: int = Query(default=20, ge=1, le=100),
               db: Session = Depends(get_db)):
    return service.list(db, page, size)

@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return service.get(db, user_id)
