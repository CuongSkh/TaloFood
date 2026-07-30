import friedChicken from '../assets/foods/fried-chicken-menu.jpg';
import burger from '../assets/foods/burger-menu.jpg';
import combo from '../assets/foods/combo-menu.jpg';
import fries from '../assets/foods/fries-menu.jpg';

const imageMap = {
  friedChicken,
  burger,
  combo,
  fries,
};

const formatPrice = (price) =>
  `${new Intl.NumberFormat('vi-VN').format(price)} VND`;

const ProductCard = ({ product }) => (
  <article className="product-card">
    <div className="product-card__media">
      {product.badge && (
        <span className="product-card__badge">{product.badge}</span>
      )}

      <img
        src={imageMap[product.imageKey]}
        alt={product.name}
        loading="lazy"
        style={{
          objectPosition: product.objectPosition || 'center',
        }}
      />
    </div>

    <div className="product-card__body">
      <p className="product-card__category">{product.category}</p>
      <h3>{product.name}</h3>
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