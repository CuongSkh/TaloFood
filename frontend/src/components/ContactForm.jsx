import { useState } from 'react';

const initialForm = {
  fullName: '',
  email: '',
  phone: '',
  subject: '',
  address: '',
  message: '',
  consent: false,
};

const subjects = [
  'Góp ý món ăn',
  'Phản hồi dịch vụ',
  'Hỗ trợ đơn hàng',
  'Hợp tác',
  'Khác',
];

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const phonePattern = /^\d{9,11}$/;

const ContactForm = () => {
  const [formData, setFormData] = useState(initialForm);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const validateForm = () => {
    const nextErrors = {};
    const phoneDigits = formData.phone.replace(/\s+/g, '');

    if (!formData.fullName.trim()) nextErrors.fullName = 'Vui lòng nhập họ và tên.';
    if (!formData.email.trim()) nextErrors.email = 'Vui lòng nhập email.';
    else if (!emailPattern.test(formData.email.trim())) nextErrors.email = 'Email chưa đúng định dạng.';
    if (!phoneDigits) nextErrors.phone = 'Vui lòng nhập số điện thoại.';
    else if (!phonePattern.test(phoneDigits)) nextErrors.phone = 'Số điện thoại phải gồm 9 đến 11 chữ số.';
    if (!formData.subject) nextErrors.subject = 'Vui lòng chọn chủ đề liên hệ.';
    if (!formData.message.trim()) nextErrors.message = 'Vui lòng nhập nội dung liên hệ.';
    else if (formData.message.trim().length < 10) nextErrors.message = 'Nội dung phải có ít nhất 10 ký tự.';
    if (!formData.consent) nextErrors.consent = 'Bạn cần đồng ý để TaloFood liên hệ lại.';

    return nextErrors;
  };

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setFormData((current) => ({ ...current, [name]: type === 'checkbox' ? checked : value }));
    setErrors((current) => ({ ...current, [name]: '' }));
    setSuccessMessage('');
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const nextErrors = validateForm();

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      setSuccessMessage('');
      return;
    }

    setIsSubmitting(true);
    window.setTimeout(() => {
      setSuccessMessage('Cảm ơn bạn đã liên hệ. TaloFood sẽ phản hồi trong thời gian sớm nhất.');
      setFormData(initialForm);
      setErrors({});
      setIsSubmitting(false);
    }, 500);
  };

  const fieldError = (name) => errors[name] && <p className="contact-field-error" id={`${name}-error`}>{errors[name]}</p>;

  return (
    <section className="contact-form-section">
      <div className="container">
        <div className="contact-form-card">
          <div className="contact-form-card__heading">
            <p className="eyebrow">KẾT NỐI VỚI TALOFOOD</p>
            <h2>GỬI LIÊN HỆ ĐẾN TALOFOOD</h2>
            <p>Điền thông tin bên dưới để đội ngũ TaloFood có thể hỗ trợ bạn nhanh chóng.</p>
          </div>

          {successMessage && <div className="contact-success" role="status">{successMessage}</div>}

          <form className="contact-form" onSubmit={handleSubmit} noValidate>
            <div className="contact-form__grid">
              <div className="contact-field">
                <label htmlFor="fullName">Họ và tên <span>*</span></label>
                <input id="fullName" name="fullName" value={formData.fullName} onChange={handleChange} aria-invalid={Boolean(errors.fullName)} aria-describedby={errors.fullName ? 'fullName-error' : undefined} placeholder="Nhập họ và tên của bạn" />
                {fieldError('fullName')}
              </div>

              <div className="contact-field">
                <label htmlFor="email">Email <span>*</span></label>
                <input id="email" name="email" type="email" value={formData.email} onChange={handleChange} aria-invalid={Boolean(errors.email)} aria-describedby={errors.email ? 'email-error' : undefined} placeholder="Nhập địa chỉ email" />
                {fieldError('email')}
              </div>

              <div className="contact-field">
                <label htmlFor="phone">Số điện thoại <span>*</span></label>
                <input id="phone" name="phone" inputMode="numeric" value={formData.phone} onChange={handleChange} aria-invalid={Boolean(errors.phone)} aria-describedby={errors.phone ? 'phone-error' : undefined} placeholder="Ví dụ: 0901234567" />
                {fieldError('phone')}
              </div>

              <div className="contact-field">
                <label htmlFor="subject">Chủ đề liên hệ <span>*</span></label>
                <select id="subject" name="subject" value={formData.subject} onChange={handleChange} aria-invalid={Boolean(errors.subject)} aria-describedby={errors.subject ? 'subject-error' : undefined}>
                  <option value="">Chọn chủ đề</option>
                  {subjects.map((subject) => <option key={subject} value={subject}>{subject}</option>)}
                </select>
                {fieldError('subject')}
              </div>

              <div className="contact-field contact-field--full">
                <label htmlFor="address">Địa chỉ hoặc khu vực của bạn</label>
                <input id="address" name="address" value={formData.address} onChange={handleChange} placeholder="Nhập địa chỉ hoặc khu vực" />
              </div>

              <div className="contact-field contact-field--full">
                <label htmlFor="message">Nội dung bạn muốn liên hệ <span>*</span></label>
                <textarea id="message" name="message" rows="6" value={formData.message} onChange={handleChange} aria-invalid={Boolean(errors.message)} aria-describedby={errors.message ? 'message-error' : undefined} placeholder="Nhập nội dung bạn muốn gửi đến TaloFood..." />
                {fieldError('message')}
              </div>
            </div>

            <div className="contact-consent">
              <label>
                <input type="checkbox" name="consent" checked={formData.consent} onChange={handleChange} />
                <span>Tôi đồng ý cung cấp thông tin để TaloFood liên hệ lại.</span>
              </label>
              {fieldError('consent')}
            </div>

            <button className="contact-submit" type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'ĐANG GỬI...' : 'GỬI LIÊN HỆ'}
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default ContactForm;
