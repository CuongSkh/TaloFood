# TaloFood Frontend — Session 7

## Run

```bash
npm install
npm run dev
```

Copy `.env.example` to `.env` only when a custom API URL is needed.

- Frontend: http://localhost:5173
- Backend expected at: http://localhost:8000
- Swagger: http://localhost:8000/docs

The Menu and Product Detail pages load products through Axios from the FastAPI backend.

## Session 13–14

Các route mới:

```text
/payment/stripe/success
/payment/stripe/cancel
/admin
/admin/products
/admin/categories
/admin/orders
/admin/users
/admin/payments
```

Chạy frontend:

```powershell
cd frontend
npm install
npm run dev
npm run build
```
