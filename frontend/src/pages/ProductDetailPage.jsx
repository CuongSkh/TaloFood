import { useCallback, useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { productsApi } from '../api/productsApi';
import { formatPrice, getProductImage } from '../components/ProductCard';
import { handleProductImageError } from '../utils/productImage';

const ProductDetailPage = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notFound, setNotFound] = useState(false);

  const loadProduct = useCallback(async () => {
    setLoading(true);
    setError('');
    setNotFound(false);
    try {
      setProduct(await productsApi.getById(id));
    } catch (requestError) {
      setProduct(null);
      if (requestError.response?.status === 404) setNotFound(true);
      else setError(requestError.userMessage || 'Không thể tải thông tin món ăn.');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { loadProduct(); }, [loadProduct]);

  if (loading) {
    return <main className="detail-page container"><div className="detail-status">Đang tải thông tin món ăn...</div></main>;
  }

  if (notFound) {
    return (
      <main className="detail-page container">
        <div className="detail-not-found">
          <p className="eyebrow">Không tìm thấy</p>
          <h1>Không tìm thấy món ăn.</h1>
          <p>Món bạn đang tìm có thể đã được cập nhật hoặc không còn trong thực đơn.</p>
          <Link className="button button--primary" to="/products">Quay lại thực đơn</Link>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="detail-page container">
        <div className="detail-not-found" role="alert">
          <p className="eyebrow">Lỗi kết nối</p>
          <h1>Không thể tải món ăn.</h1>
          <p>{error}</p>
          <button className="button button--primary" type="button" onClick={loadProduct}>Thử lại</button>
          <Link className="detail-page__back" to="/products">← Quay lại thực đơn</Link>
        </div>
      </main>
    );
  }

  return (
    <main className="detail-page container">
      <Link className="detail-page__back" to="/products">← Quay lại thực đơn</Link>
      <article className="product-detail">
        <div className="product-detail__media">
          {product.badge && <span className="product-card__badge">{product.badge}</span>}
          <img
            src={getProductImage(product)}
            alt={product.name}
            onError={handleProductImageError}
            style={{ objectPosition: product.objectPosition || 'center' }}
          />
        </div>
        <div className="product-detail__content">
          <p className="product-card__category">{product.category}</p>
          <h1>{product.name}</h1>
          <strong className="product-detail__price">{formatPrice(product.price)}</strong>
          <p className={`product-availability ${product.available ? 'is-available' : 'is-unavailable'}`}>
            {product.available ? 'Còn bán' : 'Tạm hết hàng'}
          </p>
          <p className="product-detail__description">{product.description}</p>
          <button type="button" className="button button--primary" disabled={!product.available}>+ THÊM MÓN</button>
        </div>
      </article>
    </main>
  );
};

export default ProductDetailPage;
