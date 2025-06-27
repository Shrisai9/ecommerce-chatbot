from flask import Flask
from flask_cors import CORS
from database import db, init_db
from routes.product_routes import product_bp
from routes.chat_routes import chat_bp   # <-- already has /api/chat
from routes.auth_routes import auth_bp
from routes.cart_routes import cart_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

API_KEY = "57fdfe9cdd15594c4c3ac0ec6a52402635c2c598dccacd3f865b215851ca61ae"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Shri%403109@localhost/ecommerce_chatbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = API_KEY
app.config["JWT_SECRET_KEY"] = API_KEY
app.config["JWT_TOKEN_LOCATION"] = ["headers"]


db.init_app(app)
with app.app_context():
    init_db()

jwt = JWTManager(app)
app.register_blueprint(product_bp)
app.register_blueprint(chat_bp)   # this provides /api/chat
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)


if __name__ == '__main__':
    app.run(debug=True)
