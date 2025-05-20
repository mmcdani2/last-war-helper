from flask import Flask
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
