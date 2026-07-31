import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { cartApi } from '../api/cartApi';
import { useAuth } from './AuthContext';
const CartContext=createContext(null);
const EMPTY={id:null,items:[],total_items:0,total_quantity:0,subtotal:0,delivery_fee:0,total_amount:0};
export const CartProvider=({children})=>{
  const {isAuthenticated,isAuthLoading}=useAuth();
  const [cart,setCart]=useState(EMPTY); const [loading,setLoading]=useState(false); const [error,setError]=useState('');
  const fetchCart=useCallback(async()=>{ if(!isAuthenticated){setCart(EMPTY);return EMPTY;} setLoading(true);setError('');try{const data=await cartApi.get();setCart(data);return data;}catch(e){setError(e.userMessage||'Không thể tải giỏ hàng.');throw e;}finally{setLoading(false)}},[isAuthenticated]);
  useEffect(()=>{if(!isAuthLoading){if(isAuthenticated) fetchCart(); else setCart(EMPTY)}},[isAuthenticated,isAuthLoading,fetchCart]);
  const action=useCallback(async(fn)=>{setError('');const data=await fn();setCart(data);return data;},[]);
  const value=useMemo(()=>({cart,items:cart.items||[],totalQuantity:cart.total_quantity||0,subtotal:cart.subtotal||0,deliveryFee:cart.delivery_fee||0,totalAmount:cart.total_amount||0,loading,error,fetchCart,addItem:(id,q)=>action(()=>cartApi.add(id,q)),updateItem:(id,q)=>action(()=>cartApi.update(id,q)),removeItem:(id)=>action(()=>cartApi.remove(id)),clearCart:()=>action(()=>cartApi.clear()),resetCart:()=>setCart(EMPTY)}),[cart,loading,error,fetchCart,action]);
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
};
export const useCart=()=>{const c=useContext(CartContext);if(!c) throw new Error('useCart phải dùng trong CartProvider');return c;};
