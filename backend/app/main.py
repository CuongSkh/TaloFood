import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import ALLOWED_ORIGINS, IMAGE_DIR
from app.core.database import Base, SessionLocal, engine
from app.models import Category, Product, User  # noqa: F401
from app.routers.categories import router as categories_router
from app.routers.products import router as products_router
from app.routers.users import router as users_router
from app.seed import seed_database

logger = logging.getLogger('talofood')

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            seed_database(db)
        logger.info('PostgreSQL đã kết nối và seed dữ liệu an toàn.')
    except SQLAlchemyError:
        logger.exception('Không thể kết nối hoặc khởi tạo PostgreSQL. Kiểm tra DATABASE_URL và dịch vụ PostgreSQL.')
        raise
    yield

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
app = FastAPI(title='TaloFood API', version='2.0.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=True,
                   allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], allow_headers=['*'])
app.mount('/images', StaticFiles(directory=IMAGE_DIR), name='images')
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(users_router)

@app.get('/', tags=['System'])
def root():
    return {'message': 'TaloFood API is running'}

@app.get('/health', tags=['System'])
def health():
    try:
        with SessionLocal() as db:
            db.execute(text('SELECT 1'))
        return {'status': 'ok', 'database': 'connected'}
    except SQLAlchemyError:
        return {'status': 'degraded', 'database': 'disconnected'}
