# backend/inventory_seed.py
import random, csv, os
from app import app
from database import db
from models.product import Product

DATA = [
    # name, category, price, stock, image_url
    ("iPhone 15", "Mobile", 79999, 12,
     "https://images.unsplash.com/photo-iphone.jpg"),
    ("Samsung Galaxy S24", "Mobile", 69999, 18,
     "https://images.unsplash.com/photo-galaxy.jpg"),
    ("Asus ROG Laptop", "Laptop", 119999, 7,
     "https://images.unsplash.com/photo-asus.jpg"),
    ("HP Pavilion x360", "Laptop", 64999, 10,
     "https://images.unsplash.com/photo-hp.jpg"),
    ("Sony WH-1000XM5", "Headphone", 29999, 30,
     "https://images.unsplash.com/photo-sony.jpg"),
    ("Canon EOS R50", "Camera", 55999, 5,
     "https://images.unsplash.com/photo-canon.jpg"),
]

# Generate another 100 random items
CATEGORIES = ["Mobile", "Laptop", "Headphone", "Camera", "Accessory"]
PLACEHOLDER = "https://picsum.photos/seed/{}/300/200"

for i in range(1, 101):
    cat = random.choice(CATEGORIES)
    DATA.append((
        f"{cat} Model {i}",
        cat,
        random.randint(5000, 90000),
        random.randint(5, 40),
        PLACEHOLDER.format(i)
    ))

with app.app_context():
    db.drop_all()
    db.create_all()
    for row in DATA:
        p = Product(
            name=row[0],
            category=row[1],
            description=f"High-quality {row[1]}",
            price=row[2],
            stock=row[3],
            image_url=row[4]
        )
        db.session.add(p)
    db.session.commit()
    print(f"✓  Seeded {len(DATA)} products.")
