import { useEffect, useRef, useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import BrandLogo from './BrandLogo';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

const navItems = [
  { id: 'home', label: 'Trang chủ', to: '/', end: true },
  { id: 'menu', label: 'Menu', to: '/products' },
  { id: 'blog', label: 'Blog', to: '/blog' },
  { id: 'about', label: 'About', to: '/about' },
  { id: 'contact', label: 'Liên hệ', to: '/contact' },
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
  const [accountOpen, setAccountOpen] = useState(false);
  const accountRef = useRef(null);
  const navigate = useNavigate();
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const { totalQuantity } = useCart();
  const closeMenu = () => setIsOpen(false);

  useEffect(() => {
    const closeOnOutside = (event) => {
      if (accountRef.current && !accountRef.current.contains(event.target)) setAccountOpen(false);
    };
    document.addEventListener('mousedown', closeOnOutside);
    return () => document.removeEventListener('mousedown', closeOnOutside);
  }, []);

  const handleLogout = () => {
    logout();
    setAccountOpen(false);
    navigate('/');
  };

  return (
    <header className="site-header" id="top">
      <div className="container site-header__inner">
        <BrandLogo />
        <nav className={`main-nav${isOpen ? ' main-nav--open' : ''}`} aria-label="Điều hướng chính">
          {navItems.map((item) => (
            <NavLink
              key={item.id}
              to={item.to}
              end={item.end}
              className={({ isActive }) => `main-nav__link${isActive ? ' main-nav__link--active' : ''}`}
              onClick={closeMenu}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="header-actions" aria-label="Tài khoản và giỏ hàng">
          <div className="account-menu" ref={accountRef}>
            {isAuthenticated ? (
              <button
                type="button"
                className="account-trigger"
                aria-expanded={accountOpen}
                onClick={() => setAccountOpen((value) => !value)}
              >
                <span className="account-trigger__icon"><UserIcon /></span>
                <span className="account-trigger__name">{user.full_name.split(' ').slice(-1)[0]}</span>
              </button>
            ) : (
              <Link className="account-login-link" to="/login" aria-label="Đăng nhập">
                <UserIcon /><span>Đăng nhập</span>
              </Link>
            )}
            {isAuthenticated && accountOpen && (
              <div className="account-dropdown">
                <div className="account-dropdown__identity">
                  <strong>{user.full_name}</strong>
                  <span>{user.email}</span>
                </div>
                <Link to="/profile" onClick={() => setAccountOpen(false)}>Tài khoản của tôi</Link>
                <Link to="/orders" onClick={() => setAccountOpen(false)}>Đơn hàng của tôi</Link>
                {isAdmin && <Link to="/admin" onClick={() => setAccountOpen(false)}>Quản trị</Link>}
                <button type="button" onClick={handleLogout}>Đăng xuất</button>
              </div>
            )}
          </div>

          <Link to="/cart" className="icon-button icon-button--cart" aria-label="Giỏ hàng">
            <CartIcon />
            {totalQuantity > 0 && <span>{totalQuantity > 99 ? '99+' : totalQuantity}</span>}
          </Link>
          <button
            className={`menu-toggle${isOpen ? ' menu-toggle--open' : ''}`}
            type="button"
            aria-label={isOpen ? 'Đóng menu' : 'Mở menu'}
            aria-expanded={isOpen}
            onClick={() => setIsOpen((value) => !value)}
          >
            <span /><span /><span />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
