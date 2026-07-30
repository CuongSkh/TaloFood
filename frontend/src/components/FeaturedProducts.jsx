import ProductList from './ProductList';

const FeaturedProducts = ({ products }) => (
  <section className="section products-section" id="menu">
    <div className="container">
      <div className="section-heading section-heading--row">
        <div>
          <h2>MÓN NGON PHẢI THỬ</h2>
          <p>Khám phá những hương vị được yêu thích nhất tại hệ thống TaloFood.</p>
        </div>
        <a href="#menu">Xem tất cả →</a>
      </div>
      <ProductList products={products} />
    </div>
  </section>
);

export default FeaturedProducts;
