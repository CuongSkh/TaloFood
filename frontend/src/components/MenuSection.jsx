import ProductList from './ProductList';

const MenuSection = ({ category, products, sectionRef }) => (
  <section id={category.id} ref={sectionRef} className="menu-section">
    <div className="menu-section__heading">
      <h2>{category.label}</h2>
      <span>{products.length} món</span>
    </div>
    <ProductList products={products} />
  </section>
);

export default MenuSection;
