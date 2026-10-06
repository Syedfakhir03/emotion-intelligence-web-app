"""Application factory for the Emotion Intelligence web app."""

from flask import Flask


def create_app():
    """Create and configure the Flask application."""

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    from app.routes import register_routes

    register_routes(app)

    return app