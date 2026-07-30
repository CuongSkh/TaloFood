import { Link } from 'react-router-dom';

const categories = [
  { name: 'Gà Rán', icon: '🍗', categoryId: 'ga-ran' },
  { name: 'Burger', icon: '🍔', categoryId: 'burger' },
  { name: 'Khoai Tây', icon: '🍟', categoryId: 'thuc-an-nhe' },
  { name: 'Nước Ngọt', icon: '🥤', categoryId: 'thuc-uong' },
  { name: 'Combo', icon: '🥡', categoryId: 'combo' },
];

const CategoryQuickLinks = () => (
  <section className="category-strip" aria-label="Danh mục món ăn">
    <div className="container category-strip__list">
      {categories.map((category) => (
        <Link
          key={category.name}
          className="category-chip"
          to={`/products#${category.categoryId}`}
        >
          <span className="category-chip__icon" aria-hidden="true">{category.icon}</span>
          <span>{category.name}</span>
        </Link>
      ))}
    </div>
  </section>
);

export default CategoryQuickLinks;
