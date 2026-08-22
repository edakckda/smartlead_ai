import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import config_by_name
from app.database import init_db
from app.routes import api_bp, pages_bp


def create_app():
    app = Flask(__name__)

    environment = os.environ.get("FLASK_ENV", "development")
    config_class = config_by_name.get(
        environment,
        config_by_name["development"]
    )

    app.config.from_object(config_class)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"]
            }
        }
    )

    init_db(app)

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "aktif"
        }), 200

    return app