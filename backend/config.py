import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)
print(env_path)
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallbacksecret")
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{db_user}:{db_password}"
        f"@{db_host}/{db_name}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: Mail config fallback
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")