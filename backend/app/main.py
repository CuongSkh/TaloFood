import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import ALLOWED_ORIGINS, IMAGE_DIR
from app.core.database import SessionLocal
from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router
from app.routers.products import router as products_router
from app.routers.users import router as users_router

logger = logging.getLogger('talofood')


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with SessionLocal() as db:
            db.execute(text('SELECT 1'))
        logger.info('PostgreSQL đã kết nối. Hãy dùng Alembic và script seed để quản lý dữ liệu.')
    except SQLAlchemyError:
        logger.exception('Không thể kết nối PostgreSQL. Kiểm tra DATABASE_URL và dịch vụ PostgreSQL.')
        raise
    yield


IMAGE_DIR.mkdir(parents=True, exist_ok=True)
app = FastAPI(title='TaloFood API', version='3.0.0', lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allow_headers=['*'],
)
app.mount('/images', StaticFiles(directory=IMAGE_DIR), name='images')
app.include_router(auth_router)
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
