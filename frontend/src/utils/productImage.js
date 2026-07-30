import friedChicken from '../assets/foods/fried-chicken-menu.jpg';
import { API_BASE_URL } from '../api/axiosClient';

export const PRODUCT_PLACEHOLDER = friedChicken;

export const getProductImageUrl = (imageUrl) => {
  if (!imageUrl) return PRODUCT_PLACEHOLDER;
  if (/^https?:\/\//i.test(imageUrl)) return imageUrl;
  if (imageUrl.startsWith('/images/')) return `${API_BASE_URL}${imageUrl}`;
  return PRODUCT_PLACEHOLDER;
};

export const handleProductImageError = (event) => {
  if (event.currentTarget.src !== PRODUCT_PLACEHOLDER) {
    event.currentTarget.src = PRODUCT_PLACEHOLDER;
  }
};
