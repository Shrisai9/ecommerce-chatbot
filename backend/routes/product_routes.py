from flask import Blueprint, jsonify, request
from models.product import Product
from database import db

product_bp = Blueprint('product_bp', __name__, url_prefix='/api/products')

# GET all products
@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

# GET a specific product by ID
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({"error": "Product not found"}), 404

# POST a new product
@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            stock=int(data['stock'])
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PUT to update a product
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = float(data.get('price', product.price))
    product.stock = int(data.get('stock', product.stock))

    db.session.commit()
    return jsonify(product.to_dict()), 200

# DELETE a product
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
