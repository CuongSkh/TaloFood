import { useState } from 'react';
import BrandLogo from './BrandLogo';

const navItems = [
  { id: 'home', label: 'Trang chủ', href: '#top' },
  { id: 'menu', label: 'Menu', href: '#menu' },
  { id: 'promotion', label: 'Khuyến mãi', href: '#newsletter' },
  { id: 'about', label: 'Về TaloFood', href: '#features' },
  { id: 'contact', label: 'Liên hệ', href: '#footer' },
];

const UserIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <circle cx="12" cy="8" r="3.25" />
    <path d="M5.75 19c.65-3.3 2.72-5 6.25-5s5.6 1.7 6.25 5" />
  </svg>
);

const CartIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="M3.5 4.5h2l1.8 9.2h9.9l2-6.2H7" />
    <circle cx="9" cy="18.5" r="1.2" />
    <circle cx="17" cy="18.5" r="1.2" />
  </svg>
);

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const closeMenu = () => setIsOpen(false);

  return (
    <header className="site-header" id="top">
      <div className="container site-header__inner">
        <BrandLogo />

        <nav
          className={`main-nav${isOpen ? ' main-nav--open' : ''}`}
          aria-label="Điều hướng chính"
        >
          {navItems.map((item, index) => (
            <a
              key={item.id}
              className={`main-nav__link${
                index === 0 ? ' main-nav__link--active' : ''
              }`}
              href={item.href}
              onClick={closeMenu}
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div className="header-actions" aria-label="Tài khoản và giỏ hàng">
          <button type="button" className="icon-button" aria-label="Tài khoản">
            <UserIcon />
          </button>

          <button
            type="button"
            className="icon-button icon-button--cart"
            aria-label="Giỏ hàng"
          >
            <CartIcon />
          </button>

          <button
            className={`menu-toggle${isOpen ? ' menu-toggle--open' : ''}`}
            type="button"
            aria-label={isOpen ? 'Đóng menu' : 'Mở menu'}
            aria-expanded={isOpen}
            onClick={() => setIsOpen((value) => !value)}
          >
            <span />
            <span />
            <span />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;