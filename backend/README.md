# TaloFood Backend — Session 9–10

FastAPI + PostgreSQL + SQLAlchemy + JWT Authentication cho TaloFood.

## Yêu cầu

- Windows 11
- Python 3.13
- PostgreSQL đang chạy
- Database `talofood_db` đã được tạo

## Cấu hình `.env`

Sao chép `.env.example` thành `.env` và cập nhật các giá trị local:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/talofood_db
JWT_SECRET_KEY=change_me_to_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ADMIN_EMAIL=admin@talofood.local
ADMIN_PASSWORD=change_me
ADMIN_FULL_NAME=TaloFood Admin
```

Không đưa `.env` lên Git. Không dùng secret mẫu khi triển khai production.

## Cài đặt trên Windows PowerShell

```powershell
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Migration và dữ liệu seed

```powershell
alembic upgrade head
python -m app.seed
python -m app.seed_admin
```

- `app.seed` tạo an toàn 6 category và 18 món nếu database chưa có dữ liệu.
- `app.seed_admin` lấy thông tin admin từ `.env`, không tạo trùng và không ghi đè mật khẩu admin đã tồn tại.

## Chạy backend

```powershell
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Luồng xác thực

1. Đăng ký tại `POST /auth/register`.
2. Đăng nhập tại `POST /auth/login` bằng JSON email/password.
3. Sao chép `access_token` từ response.
4. Trong Swagger bấm **Authorize** và nhập token Bearer.
5. Kiểm tra phiên bằng `GET /auth/me`.

## Phân quyền endpoint

### Public

- `GET /`, `GET /health`
- `POST /auth/register`, `POST /auth/login`
- `GET /products`, `GET /products/{id}`
- `GET /categories`, `GET /categories/{id}`
- `/images/*`

### CUSTOMER hoặc ADMIN đã đăng nhập

- `GET /auth/me`
- `GET /users/me`
- `PATCH /users/me`

### Chỉ ADMIN

- `POST /products`
- `PUT /products/{id}`
- `DELETE /products/{id}`
- `POST /products/upload-image`
- `POST /users`
- `GET /users`
- `GET /users/{id}`
- `PATCH /users/{id}/status`
- `PATCH /users/{id}/role`

## Chạy frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend mặc định gọi `http://localhost:8000`. Có thể tạo `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```
