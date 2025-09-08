from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.cart import Cart, CartItem
from models.product import Product
from models.user import User  # asumiendo que manejas usuarios
from typing import List

router = APIRouter()

def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    return user


@router.get("/", response_model=dict)
async def get_user_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return {"cart_id": cart.id, "items": cart.items}


@router.post("/items")
async def add_item_to_cart(product_id: int, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    return {"message": "Producto agregado al carrito"}


@router.put("/items/{item_id}")
async def update_cart_item(item_id: int, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_item = db.query(CartItem).join(Cart).filter(CartItem.id == item_id, Cart.user_id == current_user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item no encontrado en el carrito")

    cart_item.quantity = quantity
    db.commit()
    return {"message": "Cantidad actualizada"}


@router.delete("/items/{item_id}")
async def remove_item_from_cart(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_item = db.query(CartItem).join(Cart).filter(CartItem.id == item_id, Cart.user_id == current_user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item eliminado del carrito"}


@router.delete("/")
async def clear_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return {"message": "Carrito limpiado"}
