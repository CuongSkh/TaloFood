import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / '.env')

DATABASE_URL = os.getenv('DATABASE_URL', '').strip()
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL chưa được cấu hình. Hãy tạo backend/.env từ .env.example.')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '').strip()
if not JWT_SECRET_KEY:
    raise RuntimeError('JWT_SECRET_KEY chưa được cấu hình. Hãy bổ sung vào backend/.env.')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256').strip() or 'HS256'
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))
except ValueError as exc:
    raise RuntimeError('ACCESS_TOKEN_EXPIRE_MINUTES phải là số nguyên.') from exc

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@talofood.local').strip().casefold()
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '').strip()
ADMIN_FULL_NAME = os.getenv('ADMIN_FULL_NAME', 'TaloFood Admin').strip()

DATA_FILE = BASE_DIR / 'data' / 'products.json'
IMAGE_DIR = BASE_DIR / 'data_images'
ALLOWED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173']
CATEGORIES = ('Món mới', 'Combo', 'Gà rán', 'Burger', 'Thức ăn nhẹ', 'Thức uống')
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024

try:
    DELIVERY_FEE = __import__('decimal').Decimal(os.getenv('DELIVERY_FEE', '20000'))
except Exception as exc:
    raise RuntimeError('DELIVERY_FEE phải là số hợp lệ.') from exc

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '').strip()
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '').strip()
STRIPE_SUCCESS_URL = os.getenv('STRIPE_SUCCESS_URL', 'http://localhost:5173/payment/stripe/success').strip()
STRIPE_CANCEL_URL = os.getenv('STRIPE_CANCEL_URL', 'http://localhost:5173/payment/stripe/cancel').strip()
STRIPE_CURRENCY = (os.getenv('STRIPE_CURRENCY', 'vnd').strip() or 'vnd').lower()
