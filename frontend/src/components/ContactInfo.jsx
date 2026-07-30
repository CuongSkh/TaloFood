const icons = {
  location: (
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s6-5.2 6-11a6 6 0 1 0-12 0c0 5.8 6 11 6 11Z"/><circle cx="12" cy="10" r="2.2"/></svg>
  ),
  email: (
    <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>
  ),
  phone: (
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.2 3.8 4.8 5.1c-.8.4-1.2 1.3-.9 2.2 1.8 6.3 6.5 11 12.8 12.8.9.3 1.8-.1 2.2-.9l1.3-2.4c.4-.8.2-1.8-.6-2.3l-2.9-1.8c-.7-.4-1.5-.3-2.1.2l-1.5 1.3a14.2 14.2 0 0 1-3.3-3.3l1.3-1.5c.5-.6.6-1.4.2-2.1L9.5 4.4c-.5-.8-1.5-1-2.3-.6Z"/></svg>
  ),
  clock: (
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>
  ),
};

const contactItems = [
  { id: 'address', icon: 'location', label: 'Địa chỉ', value: 'TaloFood, Thành phố Hồ Chí Minh, Việt Nam' },
  { id: 'email', icon: 'email', label: 'Email', value: 'support@talofood.vn', href: 'mailto:support@talofood.vn' },
  { id: 'phone', icon: 'phone', label: 'Điện thoại', value: '1900 0000', href: 'tel:19000000' },
  { id: 'hours', icon: 'clock', label: 'Giờ làm việc', value: '08:00 - 22:00, tất cả các ngày trong tuần' },
];

const ContactInfo = () => (
  <section className="contact-info" aria-label="Thông tin liên hệ nhanh">
    <div className="container contact-info__grid">
      {contactItems.map((item) => (
        <article className="contact-info-card" key={item.id}>
          <span className="contact-info-card__icon">{icons[item.icon]}</span>
          <div>
            <h2>{item.label}</h2>
            {item.href ? <a href={item.href}>{item.value}</a> : <p>{item.value}</p>}
          </div>
        </article>
      ))}
    </div>
  </section>
);

export default ContactInfo;
