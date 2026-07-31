import axiosClient from './axiosClient';

export const authApi = {
  async register(payload) {
    const response = await axiosClient.post('/auth/register', payload);
    return response.data;
  },
  async login(payload) {
    const response = await axiosClient.post('/auth/login', payload);
    return response.data;
  },
  async me() {
    const response = await axiosClient.get('/auth/me');
    return response.data;
  },
  async updateProfile(payload) {
    const response = await axiosClient.patch('/users/me', payload);
    return response.data;
  },
};
