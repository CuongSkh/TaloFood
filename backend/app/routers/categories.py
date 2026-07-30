from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryResponse

router = APIRouter(prefix='/categories', tags=['Categories'])
repository = CategoryRepository()

@router.get('', response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return repository.list(db)

@router.get('/{category_id}', response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = repository.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Không tìm thấy nhóm món')
    return category
