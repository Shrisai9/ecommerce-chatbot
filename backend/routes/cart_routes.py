from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.cart import CartItem
from models.product import Product
from models.order import Order, OrderItem
from database import db

cart_bp = Blueprint("cart_bp", __name__, url_prefix="/api/cart")

@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_cart():
    uid = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=uid).all()
    return jsonify([
        {
            "id": c.id,
            "product_id": c.product_id,
            "name": c.product.name,
            "price": c.product.price,
            "quantity": c.quantity
        } for c in items
    ])

@cart_bp.route("/", methods=["POST"])
@jwt_required()
def add_item():
    uid = get_jwt_identity()
    pid = request.json["product_id"]
    qty = request.json.get("quantity", 1)

    item = CartItem.query.filter_by(user_id=uid, product_id=pid).first()
    if item:
        item.quantity += qty
    else:
        item = CartItem(user_id=uid, product_id=pid, quantity=qty)
        db.session.add(item)
    db.session.commit()
    return jsonify(msg="Added"), 201

@cart_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    uid = get_jwt_identity()
    item = CartItem.query.filter_by(id=item_id, user_id=uid).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify(msg="Removed")

# ----- checkout -----
@cart_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    uid = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=uid).all()
    if not items:
        return jsonify(msg="Cart empty"), 400

    total = sum(i.quantity * i.product.price for i in items)
    order = Order(user_id=uid, total=total)
    db.session.add(order)
    db.session.flush()          # get order.id

    for i in items:
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=i.product_id,
            quantity=i.quantity,
            price=i.product.price
        ))
        db.session.delete(i)     # empty cart
    db.session.commit()

    return jsonify(msg="Order placed", order_id=order.id, total=total)
