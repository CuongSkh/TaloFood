from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product

class CategoryRepository:
    def list(self, db: Session):
        return list(db.scalars(select(Category).order_by(Category.id)).all())

    def get(self, db: Session, category_id: int):
        return db.get(Category, category_id)

    def get_by_name(self, db: Session, name: str):
        return db.scalar(select(Category).where(Category.name == name))

    def product_count(self, db: Session, category_id: int):
        return db.scalar(select(func.count(Product.id)).where(Product.category_id == category_id)) or 0
