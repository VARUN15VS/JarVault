# app/models.py
from backend.extension import db
import enum
import uuid

class RoleEnum(enum.Enum):
    ops = "ops"
    client = "client"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)