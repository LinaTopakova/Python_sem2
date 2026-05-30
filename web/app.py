from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from web.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        from web.auth.routes import auth_bp
        from web.main.routes import main_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        # Создаём таблицы, если их ещё нет
        try:
            db.create_all()
            app.logger.info("Database tables checked/created")
        except Exception as e:
            app.logger.error(f"Failed to create tables: {e}")

    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    app.logger.info("Flask application started")

    return app
