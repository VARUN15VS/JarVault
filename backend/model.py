# app/models.py
from backend.extension import db
import enum
import uuid
from datetime import datetime

class RoleEnum(enum.Enum):
    ops = "ops"
    client = "client"

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    files = db.relationship('File', backref='uploader', lazy=True)

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.String(36), primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    uploader_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow())
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)