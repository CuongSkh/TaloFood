from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload
from app.models.category import Category
from app.models.product import Product

class ProductRepository:
    def list(self, db: Session, *, search=None, category=None, min_price=None, max_price=None,
             available=None, featured=None, page=1, size=12):
        filters = []
        if category:
            filters.append(Category.name == category)
        if min_price is not None:
            filters.append(Product.price >= min_price)
        if max_price is not None:
            filters.append(Product.price <= max_price)
        if available is not None:
            filters.append(Product.available == available)
        if featured is not None:
            filters.append(Product.featured == featured)

        base = select(Product).join(Product.category).where(*filters)
        total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
        items = db.scalars(
            base.options(joinedload(Product.category))
            .order_by(Product.id)
            .offset((page - 1) * size)
            .limit(size)
        ).all()
        return list(items), total

    def get(self, db: Session, product_id: int):
        return db.scalar(select(Product).options(joinedload(Product.category)).where(Product.id == product_id))

    def create(self, db: Session, product: Product):
        db.add(product)
        db.commit()
        db.refresh(product)
        return self.get(db, product.id)

    def update(self, db: Session, product: Product):
        db.commit()
        db.refresh(product)
        return self.get(db, product.id)

    def delete(self, db: Session, product: Product):
        db.delete(product)
        db.commit()
