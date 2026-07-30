# TaloFood Backend — Session 8

Backend FastAPI sử dụng PostgreSQL + SQLAlchemy. `data/products.json` chỉ còn dùng làm dữ liệu seed ban đầu; Product CRUD đọc và ghi PostgreSQL.

## 1. Chuẩn bị PostgreSQL

Khởi động PostgreSQL và tạo database:

```sql
CREATE DATABASE talofood_db;
```

Tạo `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/talofood_db
```

## 2. Cài backend trên Windows PowerShell

```powershell
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Tạo bảng bằng Alembic

```powershell
alembic upgrade head
```

Backend cũng có `Base.metadata.create_all()` khi startup để hỗ trợ môi trường học tập, nhưng nên chạy Alembic trước trên database mới.

## 4. Seed dữ liệu

```powershell
python -m app.seed
```

Seed là idempotent: tạo đúng 6 category và chỉ import 18 món từ JSON khi bảng products chưa có dữ liệu.

## 5. Chạy backend

```powershell
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 6. Chạy frontend

```powershell
cd ..\frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

Build production:

```powershell
npm run build
```

## API Session 8

- Products: `GET/POST /products`, `GET/PUT/DELETE /products/{id}`, `POST /products/upload-image`
- Categories: `GET /categories`, `GET /categories/{id}`
- Users: `POST /users`, `GET /users`, `GET /users/{id}`

Session 8 chưa triển khai đăng nhập, JWT, phân quyền, giỏ hàng, đơn hàng hoặc thanh toán.
