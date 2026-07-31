import axiosClient from './axiosClient';
export const cartApi = {
  async get(){ return (await axiosClient.get('/cart')).data; },
  async add(productId, quantity){ return (await axiosClient.post('/cart/items',{ product_id: productId, quantity })).data; },
  async update(itemId, quantity){ return (await axiosClient.patch(`/cart/items/${itemId}`,{ quantity })).data; },
  async remove(itemId){ return (await axiosClient.delete(`/cart/items/${itemId}`)).data; },
  async clear(){ return (await axiosClient.delete('/cart')).data; },
};
