# init_db.py
from backend import create_app
from backend.extension import db
from backend.model import User

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully.")