import ProductCard from './ProductCard';

const ProductList = ({ products }) => (
  <div className="product-grid">
    {products.map((product) => (
      <ProductCard key={product.id} product={product} />
    ))}
  </div>
);

export default ProductList;
