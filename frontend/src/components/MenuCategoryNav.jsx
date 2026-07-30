import { useEffect, useRef } from 'react';

const MenuCategoryNav = ({ categories, activeId, onSelect }) => {
  const navRef = useRef(null);
  const itemRefs = useRef({});

  useEffect(() => {
    const nav = navRef.current;
    const activeItem = itemRefs.current[activeId];

    if (!nav || !activeItem) return;

    // Chỉ cuộn ngang bên trong thanh danh mục. Không dùng scrollIntoView
    // vì hàm đó có thể làm trang bị cuộn ngược theo chiều dọc.
    const itemLeft = activeItem.offsetLeft;
    const itemRight = itemLeft + activeItem.offsetWidth;
    const visibleLeft = nav.scrollLeft;
    const visibleRight = visibleLeft + nav.clientWidth;

    if (itemLeft < visibleLeft || itemRight > visibleRight) {
      const targetLeft = itemLeft - (nav.clientWidth - activeItem.offsetWidth) / 2;
      nav.scrollTo({
        left: Math.max(0, targetLeft),
        behavior: 'smooth',
      });
    }
  }, [activeId]);

  return (
    <div className="menu-category-bar">
      <div className="container">
        <nav
          ref={navRef}
          className="menu-category-nav"
          aria-label="Danh mục thực đơn"
        >
          {categories.map((category) => (
            <button
              key={category.id}
              ref={(element) => {
                itemRefs.current[category.id] = element;
              }}
              type="button"
              className={`menu-category-nav__item${activeId === category.id ? ' is-active' : ''}`}
              onClick={() => onSelect(category.id)}
              aria-current={activeId === category.id ? 'true' : undefined}
            >
              {category.label}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default MenuCategoryNav;
