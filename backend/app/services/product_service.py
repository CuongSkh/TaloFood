import math
import unicodedata
from fastapi import HTTPException
from app.core.config import CATEGORIES
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, repository: ProductRepository | None = None):
        self.repository = repository or ProductRepository()

    @staticmethod
    def _normalize(value: str) -> str:
        normalized = unicodedata.normalize("NFD", value)
        return "".join(char for char in normalized if unicodedata.category(char) != "Mn").casefold()

    def list_products(self, *, search=None, category=None, min_price=None, max_price=None,
                      available=None, featured=None, page=1, size=12):
        if category is not None and category not in CATEGORIES:
            raise HTTPException(status_code=400, detail="Nhóm món không hợp lệ")
        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(status_code=400, detail="min_price không được lớn hơn max_price")
        products = self.repository.read_all()
        if search:
            keyword = self._normalize(search.strip())
            products = [p for p in products if keyword in self._normalize(p.get("name", "")) or keyword in self._normalize(p.get("description", ""))]
        if category:
            products = [p for p in products if p.get("category") == category]
        if min_price is not None:
            products = [p for p in products if p.get("price", 0) >= min_price]
        if max_price is not None:
            products = [p for p in products if p.get("price", 0) <= max_price]
        if available is not None:
            products = [p for p in products if p.get("available", True) is available]
        if featured is not None:
            products = [p for p in products if p.get("featured", False) is featured]
        total = len(products)
        start = (page - 1) * size
        return {"items": products[start:start + size], "total": total, "page": page, "size": size,
                "totalPages": math.ceil(total / size) if total else 0}

    def get(self, product_id: int) -> dict:
        product = next((p for p in self.repository.read_all() if p.get("id") == product_id), None)
        if product is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
        return product

    def create(self, payload: ProductCreate) -> dict:
        products = self.repository.read_all()
        record = {"id": max((p.get("id", 0) for p in products), default=0) + 1, **payload.model_dump()}
        products.append(record)
        self.repository.write_all(products)
        return record

    def update(self, product_id: int, payload: ProductUpdate) -> dict:
        products = self.repository.read_all()
        index = next((i for i, p in enumerate(products) if p.get("id") == product_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
        changes = payload.model_dump(exclude_unset=True)
        products[index] = {**products[index], **changes, "id": product_id}
        self.repository.write_all(products)
        return products[index]

    def delete(self, product_id: int) -> None:
        products = self.repository.read_all()
        if not any(p.get("id") == product_id for p in products):
            raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
        self.repository.write_all([p for p in products if p.get("id") != product_id])
