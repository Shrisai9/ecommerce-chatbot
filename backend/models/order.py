# backend/models/order.py
from database import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created   = db.Column(db.DateTime, default=datetime.utcnow)
    total     = db.Column(db.Float)

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id        = db.Column(db.Integer, primary_key=True)
    order_id  = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id= db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity  = db.Column(db.Integer, default=1, nullable=False)
    price     = db.Column(db.Float, nullable=False)
