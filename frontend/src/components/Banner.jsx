import { Link } from 'react-router-dom';
import heroImage from '../assets/foods/hero-food.jpg';

const Banner = () => (
  <section className="hero-section">
    <div className="container hero-section__inner">
      <div className="hero-section__content">
        <p className="eyebrow">Hương vị trứ danh</p>
        <h1>GÀ RÁN GIÒN RỤM<br />BURGER ĐẬM VỊ</h1>
        <p>
          Trải nghiệm hương vị thức ăn nhanh đỉnh cao với nguồn nguyên liệu tươi sạch,
          công thức tẩm ướp độc quyền chỉ có tại TaloFood.
        </p>
        <div className="hero-section__actions">
          <Link className="button button--dark-red" to="/products">ĐẶT MÓN NGAY</Link>
          <Link className="button button--outline-light" to="/products">XEM MENU</Link>
        </div>
      </div>
      <div className="hero-section__media">
        <img src={heroImage} alt="Burger và gà rán TaloFood" />
      </div>
    </div>
  </section>
);

export default Banner;
