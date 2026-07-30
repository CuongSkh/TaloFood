import BrandLogo from './BrandLogo';
import commerceLogo from '../assets/bo cong thuong.gif';

const footerColumns = [
  {
    title: 'DANH MỤC',
    links: ['Thực đơn', 'Blog', 'Cửa Hàng', 'Đặt hàng online'],
  },
  {
    title: 'CHÍNH SÁCH',
    links: ['Về chúng tôi', 'Chính sách bảo mật', 'Điều khoản sử dụng'],
  },
];

const FacebookIcon = () => <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-8h2.8l.42-3.2H13.5V7.75c0-.93.26-1.56 1.6-1.56h1.7V3.33A23 23 0 0 0 14.32 3c-2.46 0-4.14 1.5-4.14 4.25V9.8H7.4V13h2.78v8h3.32Z" /></svg>;
const InstagramIcon = () => <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="4" /><circle cx="12" cy="12" r="3.5" /><circle cx="17.5" cy="6.8" r=".8" className="social-icon-fill" /></svg>;
const YoutubeIcon = () => <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12c0 2.1-.23 3.65-.7 4.65-.3.65-.82 1.17-1.47 1.47-1.25.58-5.54.58-6.83.58s-5.58 0-6.83-.58a3.1 3.1 0 0 1-1.47-1.47C3.23 15.65 3 14.1 3 12s.23-3.65.7-4.65c.3-.65.82-1.17 1.47-1.47C6.42 5.3 10.71 5.3 12 5.3s5.58 0 6.83.58c.65.3 1.17.82 1.47 1.47.47 1 .7 2.55.7 4.65Z" /><path d="m10 9 5 3-5 3V9Z" className="social-icon-fill" /></svg>;

const socialLinks = [
  { id: 'facebook', label: 'Facebook', Icon: FacebookIcon },
  { id: 'instagram', label: 'Instagram', Icon: InstagramIcon },
  { id: 'youtube', label: 'YouTube', Icon: YoutubeIcon },
];

const contactItems = [
  { id: 'address', icon: '⌖', text: '123 Đường Số 1, Quận 1, TP. Hồ Chí Minh' },
  { id: 'phone', icon: '☎', text: 'Hotline: 1900 1234' },
  { id: 'email', icon: '✉', text: 'contact@talofood.vn' },
];

const Footer = () => (
  <footer className="site-footer" id="footer">
    <div className="container site-footer__grid">
      <div className="site-footer__brand">
        <BrandLogo compact />
        <p>Hệ thống cửa hàng thức ăn nhanh hàng đầu Việt Nam. Chúng tôi cam kết mang đến những bữa ăn ngon, sạch và tiện lợi cho mọi gia đình.</p>
        <div className="social-links" aria-label="Mạng xã hội">
          {socialLinks.map(({ id, label, Icon }) => (
            <a href="#top" key={id} aria-label={label}>
              <Icon />
            </a>
          ))}
        </div>
      </div>

      {footerColumns.map((column) => (
        <div className="footer-column" key={column.title}>
          <h3>{column.title}</h3>
          {column.links.map((link) => <a href="#top" key={link}>{link}</a>)}
        </div>
      ))}

      <div className="footer-column footer-contact">
        <h3>LIÊN HỆ</h3>
        <div className="footer-contact__list">
          {contactItems.map((item) => (
            <p key={item.id}><span aria-hidden="true">{item.icon}</span>{item.text}</p>
          ))}
        </div>
        <img className="commerce-logo" src={commerceLogo} alt="Đã thông báo Bộ Công Thương" />
      </div>
    </div>
    <div className="container site-footer__bottom">
      <small>© {new Date().getFullYear()} TaloFood. All rights reserved.</small>
    </div>
  </footer>
);

export default Footer;
