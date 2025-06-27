# backend/routes/chat_routes.py
import re
from flask import Blueprint, request, jsonify
from models.product import Product

chat_bp = Blueprint("chat_bp", __name__, url_prefix="/api/chat")

# ---------- helpers ----------
def cheapest_product(category: str | None = None):
    """Return the cheapest product overall or in a category."""
    q = Product.query
    if category:
        q = q.filter(Product.category.ilike(category))
    p = q.order_by(Product.price.asc()).first()
    if not p:
        return None
    return f"{p.name} at ₹{p.price}"

def list_names(query, limit=5):
    """Comma-separated product names (max *limit*)."""
    return ", ".join(p.name for p in query.limit(limit))

# ---------- main route ----------
@chat_bp.route("/", methods=["POST"])
def chat():
    text = request.json.get("message", "").lower().strip()

    # greet
    if re.search(r"\b(hi|hello|hey)\b", text):
        return jsonify(reply=(
            "Hello! You can ask:\n"
            "• mobiles under 20000\n"
            "• show laptops\n"
            "• cheapest camera\n"
            "• cheapest item"
        ))

    # cheapest overall
    if re.search(r"\b(cheapest|lowest price)\b", text) and " " not in text.split()[0]:
        reply = cheapest_product() or "No products yet."
        return jsonify(reply=f"Our cheapest item is {reply}.")

    # cheapest <category>
    if m := re.match(r"cheapest\s+(mobile|laptop|camera|headphone|accessory)s?", text):
        cat = m.group(1).title()
        prod = cheapest_product(cat)
        return jsonify(
            reply=prod and f"Cheapest {cat.lower()} is {prod}."
            or f"No {cat.lower()}s found."
        )

    # <category> under <price>
    if m := re.match(r".*(mobile|laptop|camera|headphone|accessory)s?\s+under\s+(\d+)", text):
        cat, cap = m.group(1).title(), int(m.group(2))
        qs = (Product.query
              .filter(Product.category.ilike(cat))
              .filter(Product.price <= cap)
              .order_by(Product.price))
        cnt = qs.count()
        if cnt == 0:
            return jsonify(reply=f"No {cat.lower()}s under ₹{cap}.")
        return jsonify(reply=f"{cnt} found: {list_names(qs)}")

    # show <category>
    if m := re.match(r".*show\s+(mobile|laptop|camera|headphone|accessory)s?", text):
        cat = m.group(1).title()
        qs = Product.query.filter(Product.category.ilike(cat))
        cnt = qs.count()
        names = list_names(qs)
        return jsonify(reply=f"{cnt} {cat.lower()}s available: {names or 'None'}")

    # fallback
    return jsonify(
        reply="Sorry, I didn't get that. Try 'show laptops' or 'mobiles under 15000'."
    )
