from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from models.product import Product
    db.create_all()
