import { Link } from 'react-router-dom';
import friedChicken from '../assets/foods/fried-chicken-menu.jpg';
import burger from '../assets/foods/burger-menu.jpg';
import combo from '../assets/foods/combo-menu.jpg';
import fries from '../assets/foods/fries-menu.jpg';

const imageMap = { friedChicken, burger, combo, fries };

export const getProductImage = (product) =>
  product.imageUrl || imageMap[product.imageKey] || friedChicken;

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
        style={{ objectPosition: product.objectPosition || 'center' }}
      />
    </Link>

    <div className="product-card__body">
      <p className="product-card__category">{product.category}</p>
      <h3><Link to={`/products/${product.id}`}>{product.name}</Link></h3>
      <p className="product-card__description">{product.description}</p>

      <div className="product-card__footer">
        <strong>{formatPrice(product.price)}</strong>
        <button type="button" aria-label={`Thêm ${product.name}`}>
          <span aria-hidden="true">+</span>
        </button>
      </div>
    </div>
  </article>
);

export default ProductCard;
