# backend/models/cart.py
from database import db

class CartItem(db.Model):
    __tablename__ = "cart_items"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity   = db.Column(db.Integer, default=1, nullable=False)

    product = db.relationship("Product")
