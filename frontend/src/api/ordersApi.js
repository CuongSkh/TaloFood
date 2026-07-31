import axiosClient from './axiosClient';
export const ordersApi = {
  async create(payload){ return (await axiosClient.post('/orders',payload)).data; },
  async mine(params={}){ return (await axiosClient.get('/orders/me',{params})).data; },
  async getById(id){ return (await axiosClient.get(`/orders/${id}`)).data; },
  async cancel(id, cancelReason=''){ return (await axiosClient.patch(`/orders/${id}/cancel`,{cancel_reason:cancelReason||null})).data; },
};
