# app/__init__.py
from flask import Flask
from backend.config import Config
from backend.extension import db,jwt,mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Binding extensions to app
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    return app