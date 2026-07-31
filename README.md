
## Thông tin sinh viên

- Họ và tên: Nguyễn Hoàng Quốc Cường
- MSSV: 2200002160
- Nhóm: NH

## Giới thiệu project

TaloFood là website đặt món ăn nhanh được xây dựng theo mô hình FullStack Web.

Hệ thống hỗ trợ khách hàng xem thực đơn, xem chi tiết món, đăng ký, đăng nhập, thêm món vào giỏ hàng, đặt hàng, thanh toán khi nhận hàng hoặc thanh toán online bằng Stripe Test Mode.

Ngoài khu vực khách hàng, hệ thống còn có khu vực quản trị dành cho ADMIN để quản lý món ăn, danh mục, đơn hàng, người dùng, thanh toán và theo dõi thống kê tổng quan.

## Công nghệ sử dụng

### Frontend

- React
- Vite
- React Router
- Axios
- Context API
- HTML5
- CSS3
- JavaScript
- Font Montserrat

### Backend

- Python 3.13
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Alembic
- Stripe SDK

### Database

- PostgreSQL
- pgAdmin

## Chức năng khách hàng

- Xem trang chủ
- Xem thực đơn
- Tìm kiếm và lọc món ăn
- Xem chi tiết món
- Đăng ký tài khoản
- Đăng nhập và đăng xuất
- Xem thông tin cá nhân
- Thêm món vào giỏ hàng
- Tăng, giảm số lượng món
- Xóa món khỏi giỏ hàng
- Thanh toán khi nhận hàng COD
- Thanh toán Stripe Test Mode
- Xem lịch sử đơn hàng
- Xem chi tiết đơn hàng
- Hủy đơn khi còn ở trạng thái cho phép
- Xem Blog, About và Contact

## Chức năng quản trị

- Đăng nhập bằng tài khoản ADMIN
- Xem Dashboard thống kê
- Xem tổng sản phẩm
- Xem tổng đơn hàng
- Xem tổng người dùng
- Xem tổng doanh thu
- Xem biểu đồ doanh thu theo tháng
- Quản lý món ăn
- Thêm và sửa món
- Upload ảnh món ăn
- Bật hoặc tắt trạng thái còn bán
- Quản lý danh mục
- Quản lý đơn hàng
- Cập nhật trạng thái đơn
- Quản lý người dùng
- Khóa hoặc mở tài khoản
- Phân quyền CUSTOMER và ADMIN
- Xem lịch sử thanh toán Stripe

## Cấu trúc hệ thống

```text
TaloFood/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.js
