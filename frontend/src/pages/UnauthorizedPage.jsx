import { Link } from 'react-router-dom';

const UnauthorizedPage = () => (
  <main className="auth-route-status auth-route-status--error">
    <div>
      <p className="eyebrow">403</p>
      <h1>Bạn không có quyền truy cập</h1>
      <p>Khu vực này chỉ dành cho tài khoản quản trị TaloFood.</p>
      <Link className="button button--dark-red" to="/">Về trang chủ</Link>
    </div>
  </main>
);

export default UnauthorizedPage;
