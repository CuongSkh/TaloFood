import axiosClient from './axiosClient';
export const paymentsApi={
 createStripeSession:async(orderId)=>(await axiosClient.post('/payments/stripe/create-session',{order_id:orderId})).data,
 verifyStripe:async(sessionId)=>(await axiosClient.get('/payments/stripe/verify',{params:{session_id:sessionId}})).data,
 cancelStripe:async(orderId)=>(await axiosClient.post('/payments/stripe/cancel',{order_id:Number(orderId)})).data,
 byOrder:async(orderId)=>(await axiosClient.get(`/payments/order/${orderId}`)).data,
};
