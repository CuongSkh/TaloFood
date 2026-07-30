import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / '.env')

DATABASE_URL = os.getenv('DATABASE_URL', '').strip()
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL chưa được cấu hình. Hãy tạo backend/.env từ .env.example.')

DATA_FILE = BASE_DIR / 'data' / 'products.json'
IMAGE_DIR = BASE_DIR / 'data_images'
ALLOWED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173']
CATEGORIES = ('Món mới', 'Combo', 'Gà rán', 'Burger', 'Thức ăn nhẹ', 'Thức uống')
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
