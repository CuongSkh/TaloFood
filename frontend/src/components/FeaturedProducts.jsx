import { Link } from 'react-router-dom';
import ProductList from './ProductList';

const FeaturedProducts = ({ products }) => (
  <section className="section products-section" id="menu">
    <div className="container">
      <div className="section-heading section-heading--row">
        <div>
          <h2>MÓN NGON PHẢI THỬ</h2>
          <p>Khám phá những hương vị được yêu thích nhất tại hệ thống TaloFood.</p>
        </div>
        <Link to="/products">Xem tất cả →</Link>
      </div>
      <ProductList products={products} />
    </div>
  </section>
);

export default FeaturedProducts;
