const categories = [
  { name: 'Gà Rán', icon: '🍗' },
  { name: 'Burger', icon: '🍔' },
  { name: 'Khoai Tây', icon: '🍟' },
  { name: 'Nước Ngọt', icon: '🥤' },
  { name: 'Combo', icon: '🥡' },
];

const CategoryQuickLinks = () => (
  <section className="category-strip" aria-label="Danh mục món ăn">
    <div className="container category-strip__list">
      {categories.map((category) => (
        <a key={category.name} className="category-chip" href="#menu">
          <span className="category-chip__icon" aria-hidden="true">{category.icon}</span>
          <span>{category.name}</span>
        </a>
      ))}
    </div>
  </section>
);

export default CategoryQuickLinks;
