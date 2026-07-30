import axiosClient from './axiosClient';
import { getApiErrorMessage } from './errorHandler';

const unwrapList = (data) => ({
  items: Array.isArray(data) ? data : data?.items || [],
  total: Array.isArray(data) ? data.length : data?.total || 0,
  page: data?.page || 1,
  size: data?.size || (Array.isArray(data) ? data.length : 0),
  totalPages: data?.totalPages || 0,
});

const runRequest = async (request, fallbackMessage) => {
  try {
    const response = await request();
    return response.data;
  } catch (error) {
    error.userMessage = getApiErrorMessage(error, fallbackMessage);
    throw error;
  }
};

export const productsApi = {
  async getAll(params = {}) {
    const data = await runRequest(
      () => axiosClient.get('/products', { params }),
      'Không thể tải thực đơn.',
    );
    return unwrapList(data);
  },

  getById(id) {
    return runRequest(
      () => axiosClient.get(`/products/${id}`),
      'Không thể tải thông tin món ăn.',
    );
  },

  create(productData) {
    return runRequest(
      () => axiosClient.post('/products', productData),
      'Không thể tạo món ăn.',
    );
  },

  update(id, productData) {
    return runRequest(
      () => axiosClient.put(`/products/${id}`, productData),
      'Không thể cập nhật món ăn.',
    );
  },

  remove(id) {
    return runRequest(
      () => axiosClient.delete(`/products/${id}`),
      'Không thể xóa món ăn.',
    );
  },

  async uploadImage(file) {
    const formData = new FormData();
    formData.append('image_file', file);
    return runRequest(
      () => axiosClient.post('/products/upload-image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      }),
      'Không thể tải ảnh lên.',
    );
  },
};
