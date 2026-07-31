import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getApiErrorMessage } from '../api/errorHandler';
import { useAuth } from '../context/AuthContext';

const initialForm = { full_name: '', email: '', phone: '', password: '', confirmPassword: '' };

const RegisterPage = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const updateField = (field) => (event) => {
    setForm((current) => ({ ...current, [field]: event.target.value }));
  };

  const validate = () => {
    if (!form.full_name.trim() || !form.email.trim() || !form.password || !form.confirmPassword) {
      return 'Vui lòng nhập đầy đủ các trường bắt buộc.';
    }
    if (form.password.length < 8) return 'Mật khẩu phải có ít nhất 8 ký tự.';
    if (form.password !== form.confirmPassword) return 'Mật khẩu xác nhận không khớp.';
    return '';
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const validationMessage = validate();
    if (validationMessage) {
      setError(validationMessage);
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      await register({
        full_name: form.full_name.trim(),
        email: form.email.trim(),
        phone: form.phone.trim() || null,
        password: form.password,
      });
      navigate('/login', { replace: true, state: { registered: true } });
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, 'Đăng ký không thành công.'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-card auth-card--wide" aria-labelledby="register-title">
        <p className="auth-card__eyebrow">Gia nhập TaloFood</p>
        <h1 id="register-title">Tạo tài khoản</h1>
        <p className="auth-card__intro">Thông tin của bạn được dùng để quản lý tài khoản khách hàng.</p>
        {error && <div className="auth-alert auth-alert--error" role="alert">{error}</div>}
        <form className="auth-form auth-form--grid" onSubmit={handleSubmit} noValidate>
          <label>
            Họ và tên <span>*</span>
            <input value={form.full_name} onChange={updateField('full_name')} autoComplete="name" required />
          </label>
          <label>
            Email <span>*</span>
            <input type="email" value={form.email} onChange={updateField('email')} autoComplete="email" required />
          </label>
          <label>
            Số điện thoại
            <input value={form.phone} onChange={updateField('phone')} autoComplete="tel" />
          </label>
          <label>
            Mật khẩu <span>*</span>
            <input type="password" value={form.password} onChange={updateField('password')} autoComplete="new-password" required />
          </label>
          <label className="auth-form__full">
            Xác nhận mật khẩu <span>*</span>
            <input type="password" value={form.confirmPassword} onChange={updateField('confirmPassword')} autoComplete="new-password" required />
          </label>
          <button className="auth-submit auth-form__full" type="submit" disabled={submitting}>
            {submitting ? 'Đang tạo tài khoản...' : 'Đăng ký'}
          </button>
        </form>
        <p className="auth-card__switch">Đã có tài khoản? <Link to="/login">Đăng nhập</Link></p>
      </section>
    </main>
  );
};

export default RegisterPage;
