import { Link } from 'react-router-dom';
import { getProductImageUrl, handleProductImageError } from '../utils/productImage';

export const getProductImage = (product) => getProductImageUrl(product.imageUrl);

export const formatPrice = (price) =>
  new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    maximumFractionDigits: 0,
  }).format(price);

const ProductCard = ({ product }) => (
  <article className="product-card">
    <Link className="product-card__media" to={`/products/${product.id}`} aria-label={`Xem ${product.name}`}>
      {product.badge && <span className="product-card__badge">{product.badge}</span>}
      <img
        src={getProductImage(product)}
        alt={product.name}
        loading="lazy"
        onError={handleProductImageError}
        style={{ objectPosition: product.objectPosition || 'center' }}
      />
    </Link>

    <div className="product-card__body">
      <p className="product-card__category">{product.category}</p>
      <h3><Link to={`/products/${product.id}`}>{product.name}</Link></h3>
      <p className="product-card__description">{product.description}</p>

      <div className="product-card__footer">
        <strong>{formatPrice(product.price)}</strong>
        <button type="button" aria-label={`Thêm ${product.name}`} disabled={!product.available}>
          <span aria-hidden="true">+</span>
        </button>
      </div>
    </div>
  </article>
);

export default ProductCard;
