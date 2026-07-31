import { useEffect, useState } from 'react';
import { getApiErrorMessage } from '../api/errorHandler';
import { useAuth } from '../context/AuthContext';

const ProfilePage = () => {
  const { user, updateProfile } = useAuth();
  const [form, setForm] = useState({ full_name: '', phone: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (user) setForm({ full_name: user.full_name || '', phone: user.phone || '' });
  }, [user]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (form.full_name.trim().length < 2) {
      setError('Họ và tên phải có ít nhất 2 ký tự.');
      return;
    }
    setSubmitting(true);
    setError('');
    setMessage('');
    try {
      await updateProfile({ full_name: form.full_name.trim(), phone: form.phone.trim() || null });
      setMessage('Thông tin tài khoản đã được cập nhật.');
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, 'Không thể cập nhật tài khoản.'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="profile-page">
      <section className="container profile-card">
        <div className="profile-card__heading">
          <p className="eyebrow">Tài khoản TaloFood</p>
          <h1>Thông tin của tôi</h1>
          <span className="profile-role">{user?.role}</span>
        </div>
        {message && <div className="auth-alert auth-alert--success">{message}</div>}
        {error && <div className="auth-alert auth-alert--error">{error}</div>}
        <form className="auth-form profile-form" onSubmit={handleSubmit}>
          <label>
            Họ và tên
            <input value={form.full_name} onChange={(event) => setForm((current) => ({ ...current, full_name: event.target.value }))} />
          </label>
          <label>
            Email
            <input value={user?.email || ''} disabled />
          </label>
          <label>
            Số điện thoại
            <input value={form.phone} onChange={(event) => setForm((current) => ({ ...current, phone: event.target.value }))} />
          </label>
          <button className="auth-submit" type="submit" disabled={submitting}>
            {submitting ? 'Đang lưu...' : 'Lưu thay đổi'}
          </button>
        </form>
      </section>
    </main>
  );
};

export default ProfilePage;
