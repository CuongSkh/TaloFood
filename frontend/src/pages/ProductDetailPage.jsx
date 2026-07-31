import { useCallback, useEffect, useState } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { productsApi } from '../api/productsApi';
import { formatPrice, getProductImage } from '../components/ProductCard';
import { handleProductImageError } from '../utils/productImage';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

const ProductDetailPage = () => {
  const { id } = useParams(); const navigate=useNavigate(); const location=useLocation();
  const {isAuthenticated}=useAuth(); const {addItem}=useCart();
  const [product,setProduct]=useState(null); const [loading,setLoading]=useState(true); const [error,setError]=useState(''); const [notFound,setNotFound]=useState(false); const [quantity,setQuantity]=useState(1); const [adding,setAdding]=useState(false); const [notice,setNotice]=useState('');
  const loadProduct=useCallback(async()=>{setLoading(true);setError('');setNotFound(false);try{setProduct(await productsApi.getById(id))}catch(e){setProduct(null);if(e.response?.status===404)setNotFound(true);else setError(e.userMessage||'Không thể tải thông tin món ăn.')}finally{setLoading(false)}},[id]);
  useEffect(()=>{loadProduct()},[loadProduct]);
  const add=async()=>{if(!isAuthenticated){navigate('/login',{state:{from:location}});return}setAdding(true);setNotice('');try{await addItem(product.id,quantity);setNotice('Đã thêm món vào giỏ hàng.')}catch(e){setNotice(e.userMessage||e.response?.data?.detail||'Không thể thêm món vào giỏ.')}finally{setAdding(false)}};
  if(loading)return <main className="detail-page container"><div className="detail-status">Đang tải thông tin món ăn...</div></main>;
  if(notFound)return <main className="detail-page container"><div className="detail-not-found"><h1>Không tìm thấy món ăn.</h1><Link className="button button--primary" to="/products">Quay lại thực đơn</Link></div></main>;
  if(error)return <main className="detail-page container"><div className="detail-not-found"><h1>Không thể tải món ăn.</h1><p>{error}</p><button className="button button--primary" onClick={loadProduct}>Thử lại</button></div></main>;
  return <main className="detail-page container"><Link className="detail-page__back" to="/products">← Quay lại thực đơn</Link><article className="product-detail"><div className="product-detail__media">{product.badge&&<span className="product-card__badge">{product.badge}</span>}<img src={getProductImage(product)} alt={product.name} onError={handleProductImageError} style={{objectPosition:product.objectPosition||'center'}}/></div><div className="product-detail__content"><p className="product-card__category">{product.category}</p><h1>{product.name}</h1><strong className="product-detail__price">{formatPrice(product.price)}</strong><p className={`product-availability ${product.available?'is-available':'is-unavailable'}`}>{product.available?'Còn bán':'Tạm hết hàng'}</p><p className="product-detail__description">{product.description}</p><div className="detail-quantity"><button disabled={quantity<=1} onClick={()=>setQuantity(q=>Math.max(1,q-1))}>−</button><span>{quantity}</span><button onClick={()=>setQuantity(q=>q+1)}>+</button></div>{notice&&<div className="commerce-alert">{notice}</div>}<button type="button" className="button button--primary detail-add" disabled={!product.available||adding} onClick={add}>{adding?'Đang thêm...':`THÊM VÀO GIỎ (${formatPrice(product.price*quantity)})`}</button></div></article></main>;
};
export default ProductDetailPage;
