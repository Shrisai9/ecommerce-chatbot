# backend/models/user.py
from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Application user model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(512), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # -------- password helpers --------
    def set_password(self, raw_password: str) -> None:
        """Hash and store the password."""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Return True if provided password matches stored hash."""
        return check_password_hash(self.password_hash, raw_password)

    # -------- serialization helper ----
    def to_dict(self) -> dict:
        """Safe representation (excludes password hash)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
        }

    # -------- misc --------
    def __repr__(self):
        return f"<User {self.username}>"
