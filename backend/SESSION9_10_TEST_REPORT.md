# TaloFood Session 9–10 Test Report

## Phạm vi kiểm tra đã chạy trong môi trường xử lý

### Backend compile và cấu trúc

- Python compile cho `app/` và `alembic/`: PASS
- Import FastAPI app với cấu hình test: PASS
- OpenAPI có `/auth/register`, `/auth/login`, `/auth/me`: PASS
- Product GET là public: PASS
- Product POST có Bearer security dependency: PASS
- User list có Bearer security dependency: PASS

### Register và password

- Đăng ký customer hợp lệ: PASS
- Email được lowercase: PASS
- Role luôn `CUSTOMER`: PASS
- Password được hash Argon2, không lưu plaintext: PASS
- Verify password đúng: PASS
- Email trùng trả 409 trong service: PASS
- Response schema không chứa `password_hash`: PASS qua kiểm tra schema/source

### Login và JWT

- Login đúng trả access token: PASS
- `token_type` là `bearer`: PASS
- JWT có `sub` và `exp`: PASS
- Tài khoản bị khóa không đăng nhập được: PASS
- CUSTOMER bị `require_admin` từ chối 403: PASS
- ADMIN vượt qua `require_admin`: PASS

### Admin seed

- Tạo admin từ biến môi trường: PASS
- Password admin được hash: PASS
- Role là ADMIN: PASS
- Chạy seed lần hai không tạo trùng và không đổi mật khẩu: PASS

### Database test trong môi trường xử lý

Các test logic trên chạy bằng SQLite tạm qua cùng SQLAlchemy models/services để không phụ thuộc PostgreSQL bên ngoài.

- Tạo các model Category/Product/User: PASS
- Seed category/product hiện có: PASS
- User tồn tại sau commit/reopen session test: PASS

## Chưa thể tuyên bố PASS trong môi trường xử lý

- Kết nối PostgreSQL local `localhost:5432/talofood_db`: NOT RUN — môi trường xử lý không có PostgreSQL local của người dùng.
- `alembic upgrade head` trên PostgreSQL local: NOT RUN.
- Kiểm thử HTTP end-to-end bằng TestClient: NOT RUN vì registry nội bộ không cung cấp package bổ sung `httpx`.
- `npm install` / `npm run build`: NOT RUN SUCCESSFULLY vì npm registry nội bộ trả 404 cho dependency `zod-validation-error-4.0.2.tgz` từ lockfile hiện có.
- Kiểm thử trực quan Header/Login/Register/ProtectedRoute trên trình duyệt: cần chạy cùng backend và frontend trên máy người dùng.

## Checklist cần xác nhận trên máy Windows của người dùng

1. `alembic upgrade head` tạo migration auth mới mà không mất products/categories.
2. `python -m app.seed_admin` tạo đúng một admin.
3. Register/Login/Me chạy qua Swagger và React.
4. CUSTOMER gọi POST `/products` và GET `/users` nhận 403.
5. ADMIN gọi được các endpoint quản trị.
6. Reload frontend khôi phục phiên bằng `/auth/me`.
7. Logout xóa token.
8. `npm run build` thành công.
9. Menu, Blog, About, Contact và Footer vẫn hoạt động.
