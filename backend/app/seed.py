import json
import re
import unicodedata
from pathlib import Path
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.config import CATEGORIES, DATA_FILE
from app.core.database import Base, SessionLocal, engine
from app.models.category import Category
from app.models.product import Product

CATEGORY_DESCRIPTIONS = {
    'Món mới': 'Những món ăn mới nhất của TaloFood.',
    'Combo': 'Các phần ăn kết hợp tiện lợi và tiết kiệm.',
    'Gà rán': 'Các món gà rán giòn ngon đặc trưng.',
    'Burger': 'Burger thịt và gà với rau tươi, phô mai.',
    'Thức ăn nhẹ': 'Các món ăn kèm và món nhẹ.',
    'Thức uống': 'Đồ uống giải khát dùng kèm bữa ăn.',
}

def slugify(value: str) -> str:
    value = unicodedata.normalize('NFD', value)
    value = ''.join(c for c in value if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-zA-Z0-9]+', '-', value).strip('-').lower()

def seed_database(db: Session) -> dict:
    categories_by_name = {item.name: item for item in db.scalars(select(Category)).all()}
    for name in CATEGORIES:
        if name not in categories_by_name:
            category = Category(name=name, slug=slugify(name), description=CATEGORY_DESCRIPTIONS[name])
            db.add(category)
            db.flush()
            categories_by_name[name] = category
    db.commit()

    product_count = db.scalar(select(func.count(Product.id))) or 0
    inserted = 0
    if product_count == 0 and Path(DATA_FILE).exists():
        products = json.loads(Path(DATA_FILE).read_text(encoding='utf-8'))
        for item in products:
            category = categories_by_name.get(item['category'])
            if not category:
                continue
            db.add(Product(
                id=item.get('id'), name=item['name'], slug=f"{slugify(item['name'])}-{item.get('id')}",
                description=item['description'], price=item['price'], image_url=item.get('imageUrl', '/images/placeholder.svg'),
                badge=item.get('badge'), featured=item.get('featured', False), is_new=item.get('isNew', False),
                available=item.get('available', True), object_position=item.get('objectPosition', 'center'),
                category_id=category.id,
            ))
            inserted += 1
        db.commit()
    return {'categories': len(categories_by_name), 'products_inserted': inserted}

def main():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        result = seed_database(db)
    print(f"Seed hoàn tất: {result['categories']} categories, {result['products_inserted']} products mới.")

if __name__ == '__main__':
    main()
