from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session
from app.core.config import ALLOWED_IMAGE_TYPES, IMAGE_DIR, MAX_IMAGE_SIZE
from app.core.database import get_db
from app.schemas.product import DeleteProductResponse, ImageUploadResponse, PaginatedProductResponse, ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix='/products', tags=['Products'])
service = ProductService()

@router.get('', response_model=PaginatedProductResponse)
def list_products(search: str | None = None, category: str | None = None,
                  min_price: float | None = Query(default=None, ge=0),
                  max_price: float | None = Query(default=None, ge=0),
                  available: bool | None = None, featured: bool | None = None,
                  page: int = Query(default=1, ge=1), size: int = Query(default=12, ge=1, le=100),
                  db: Session = Depends(get_db)):
    return service.list_products(db, search=search, category=category, min_price=min_price, max_price=max_price,
                                 available=available, featured=featured, page=page, size=size)

@router.post('/upload-image', response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(image_file: UploadFile = File(...)):
    if image_file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail='Chỉ chấp nhận ảnh JPG, PNG hoặc WEBP')
    content = await image_file.read(MAX_IMAGE_SIZE + 1)
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail='Ảnh không được vượt quá 5 MB')
    extension = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp'}[image_file.content_type]
    safe_stem = ''.join(c for c in Path(image_file.filename or 'image').stem.lower() if c.isalnum() or c in '-_')[:50] or 'image'
    filename = f'{uuid4().hex}-{safe_stem}{extension}'
    try:
        (IMAGE_DIR / filename).write_bytes(content)
    except OSError as exc:
        raise HTTPException(status_code=500, detail='Không thể lưu ảnh') from exc
    return {'imageUrl': f'/images/{filename}'}

@router.get('/{product_id}', response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return service.get(db, product_id)

@router.post('', response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return service.create(db, payload)

@router.put('/{product_id}', response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    return service.update(db, product_id, payload)

@router.delete('/{product_id}', response_model=DeleteProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    service.delete(db, product_id)
    return {'message': 'Đã xóa món ăn thành công'}
