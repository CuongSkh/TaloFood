from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload
from app.core.config import DELIVERY_FEE
from app.models.cart import Cart, CartItem
from app.models.product import Product

class CartService:
    def _cart(self, db: Session, user_id: int, create=False):
        cart = db.execute(select(Cart).options(joinedload(Cart.items).joinedload(CartItem.product)).where(Cart.user_id == user_id)).unique().scalar_one_or_none()
        if not cart and create:
            cart = Cart(user_id=user_id); db.add(cart); db.flush()
        return cart
    def response(self, cart):
        if not cart:
            return {'id':None,'items':[],'total_items':0,'total_quantity':0,'subtotal':0,'delivery_fee':0,'total_amount':0}
        items=[]; subtotal=Decimal('0'); qty=0
        for item in cart.items:
            p=item.product; line=p.price*item.quantity; subtotal+=line; qty+=item.quantity
            items.append({'id':item.id,'product_id':p.id,'name':p.name,'description':p.description,'image_url':p.image_url,'unit_price':float(p.price),'quantity':item.quantity,'line_total':float(line),'available':p.available})
        fee=DELIVERY_FEE if items else Decimal('0')
        return {'id':cart.id,'items':items,'total_items':len(items),'total_quantity':qty,'subtotal':float(subtotal),'delivery_fee':float(fee),'total_amount':float(subtotal+fee)}
    def get(self, db,user_id): return self.response(self._cart(db,user_id))
    def add(self,db,user_id,product_id,quantity):
        product=db.get(Product,product_id)
        if not product: raise HTTPException(404,'Không tìm thấy món ăn')
        if not product.available: raise HTTPException(409,'Món ăn này hiện không còn phục vụ')
        cart=self._cart(db,user_id,True)
        item=next((i for i in cart.items if i.product_id==product_id),None)
        if item: item.quantity+=quantity
        else: db.add(CartItem(cart_id=cart.id,product_id=product_id,quantity=quantity))
        db.commit(); db.expire_all(); return self.get(db,user_id)
    def update(self,db,user_id,item_id,quantity):
        item=db.scalar(select(CartItem).join(Cart).where(CartItem.id==item_id,Cart.user_id==user_id))
        if not item: raise HTTPException(404,'Không tìm thấy món trong giỏ hàng')
        product=db.get(Product,item.product_id)
        if not product or not product.available: raise HTTPException(409,'Món ăn này hiện không còn phục vụ')
        item.quantity=quantity; db.commit(); db.expire_all(); return self.get(db,user_id)
    def remove(self,db,user_id,item_id):
        item=db.scalar(select(CartItem).join(Cart).where(CartItem.id==item_id,Cart.user_id==user_id))
        if not item: raise HTTPException(404,'Không tìm thấy món trong giỏ hàng')
        db.delete(item); db.commit(); db.expire_all(); return self.get(db,user_id)
    def clear(self,db,user_id):
        cart=db.scalar(select(Cart).where(Cart.user_id==user_id))
        if cart: db.execute(delete(CartItem).where(CartItem.cart_id==cart.id)); db.commit()
        return self.get(db,user_id)
