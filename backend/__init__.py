from flask import Flask
from backend.config import Config
from backend.extension import db, jwt, mail
from backend.routes.auth import auth_bp
from backend.routes.file_ops import file_ops_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(file_ops_bp, url_prefix="/api/file")

    return app

