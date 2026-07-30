import { Link, useParams } from 'react-router-dom';
import products from '../data/products.json';
import { formatPrice, getProductImage } from '../components/ProductCard';

const ProductDetailPage = () => {
  const { id } = useParams();
  const product = products.find((item) => String(item.id) === id);

  if (!product) {
    return (
      <main className="detail-page container">
        <div className="detail-not-found">
          <p className="eyebrow">Không tìm thấy</p>
          <h1>Món ăn không tồn tại</h1>
          <p>Món bạn đang tìm có thể đã được cập nhật hoặc không còn trong thực đơn.</p>
          <Link className="button button--primary" to="/products">Quay lại Thực đơn</Link>
        </div>
      </main>
    );
  }

  return (
    <main className="detail-page container">
      <Link className="detail-page__back" to="/products">← Quay lại Thực đơn</Link>
      <article className="product-detail">
        <div className="product-detail__media">
          {product.badge && <span className="product-card__badge">{product.badge}</span>}
          <img
            src={getProductImage(product)}
            alt={product.name}
            style={{ objectPosition: product.objectPosition || 'center' }}
          />
        </div>
        <div className="product-detail__content">
          <p className="product-card__category">{product.category}</p>
          <h1>{product.name}</h1>
          <strong className="product-detail__price">{formatPrice(product.price)}</strong>
          <p className="product-detail__description">{product.description}</p>
          <button type="button" className="button button--primary">+ THÊM MÓN</button>
        </div>
      </article>
    </main>
  );
};

export default ProductDetailPage;
