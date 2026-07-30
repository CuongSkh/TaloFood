import math
import re
import unicodedata
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.config import CATEGORIES
from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.categories = CategoryRepository()

    @staticmethod
    def _slugify(value: str) -> str:
        value = unicodedata.normalize('NFD', value)
        value = ''.join(c for c in value if unicodedata.category(c) != 'Mn')
        value = re.sub(r'[^a-zA-Z0-9]+', '-', value).strip('-').lower()
        return value or 'mon-an'

    @staticmethod
    def _to_response(product: Product) -> dict:
        return {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'category': product.category.name,
            'description': product.description,
            'imageUrl': product.image_url,
            'badge': product.badge,
            'featured': product.featured,
            'isNew': product.is_new,
            'available': product.available,
            'objectPosition': product.object_position,
        }

    @staticmethod
    def _normalize(value: str) -> str:
        value = unicodedata.normalize('NFD', value)
        return ''.join(c for c in value if unicodedata.category(c) != 'Mn').casefold()

    def list_products(self, db: Session, **params):
        category = params.get('category')
        if category is not None and category not in CATEGORIES:
            raise HTTPException(status_code=400, detail='Nhóm món không hợp lệ')
        if params.get('min_price') is not None and params.get('max_price') is not None and params['min_price'] > params['max_price']:
            raise HTTPException(status_code=400, detail='min_price không được lớn hơn max_price')
        search = params.pop('search', None)
        page, size = params['page'], params['size']
        if search and search.strip():
            fetch_params = {**params, 'page': 1, 'size': 100000}
            all_items, _ = self.repository.list(db, search=None, **fetch_params)
            keyword = self._normalize(search.strip())
            filtered = [item for item in all_items if keyword in self._normalize(item.name) or keyword in self._normalize(item.description)]
            total = len(filtered)
            start = (page - 1) * size
            items = filtered[start:start + size]
        else:
            items, total = self.repository.list(db, search=None, **params)
        return {'items': [self._to_response(item) for item in items], 'total': total, 'page': page, 'size': size,
                'totalPages': math.ceil(total / size) if total else 0}

    def get(self, db: Session, product_id: int):
        product = self.repository.get(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Không tìm thấy món ăn')
        return self._to_response(product)

    def create(self, db: Session, payload: ProductCreate):
        category = self.categories.get_by_name(db, payload.category)
        if not category:
            raise HTTPException(status_code=404, detail='Không tìm thấy nhóm món')
        data = payload.model_dump()
        product = Product(
            name=data['name'], slug=f"{self._slugify(data['name'])}-{uuid4().hex[:8]}",
            description=data['description'], price=data['price'], image_url=data['imageUrl'], badge=data['badge'],
            featured=data['featured'], is_new=data['isNew'], available=data['available'],
            object_position=data['objectPosition'], category_id=category.id,
        )
        try:
            return self._to_response(self.repository.create(db, product))
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=409, detail='Tên định danh món ăn đã tồn tại') from exc

    def update(self, db: Session, product_id: int, payload: ProductUpdate):
        product = self.repository.get(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Không tìm thấy món ăn')
        changes = payload.model_dump(exclude_unset=True)
        if 'category' in changes:
            category = self.categories.get_by_name(db, changes.pop('category'))
            if not category:
                raise HTTPException(status_code=404, detail='Không tìm thấy nhóm món')
            product.category_id = category.id
        field_map = {'imageUrl': 'image_url', 'isNew': 'is_new', 'objectPosition': 'object_position'}
        for key, value in changes.items():
            setattr(product, field_map.get(key, key), value)
        if 'name' in changes:
            product.slug = f"{self._slugify(product.name)}-{product.id}"
        return self._to_response(self.repository.update(db, product))

    def delete(self, db: Session, product_id: int):
        product = self.repository.get(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Không tìm thấy món ăn')
        self.repository.delete(db, product)
