import { Link } from 'react-router-dom';

const NotFoundPage = () => (
  <main className="not-found-page container">
    <p className="eyebrow">Lỗi 404</p>
    <h1>Trang không tồn tại</h1>
    <p>Đường dẫn bạn truy cập không có trong TaloFood.</p>
    <Link className="button button--primary" to="/">Về Trang chủ</Link>
  </main>
);

export default NotFoundPage;
