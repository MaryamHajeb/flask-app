"""Application factory for the Student API."""

from flask import Flask, render_template
from flask_cors import CORS

from config import Config
from app.errors import register_error_handlers
from app.extensions import db


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from app.routes.students import students_bp

    app.register_blueprint(students_bp, url_prefix="/api/students")
    register_error_handlers(app)

    @app.get("/")
    def index():
        """Serve the lightweight Student Management dashboard."""
        return render_template("index.html")

    @app.get("/api/health")
    def health_check():
        return {"status": "ok", "message": "Student API is running"}, 200

    return app
