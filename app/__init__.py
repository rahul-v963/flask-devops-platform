from flask import Flask

APP_VERSION = "1.0.0"


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def home():
        return {
            "application": "flask-devops-api",
            "version": APP_VERSION,
            "environment": "production",
        }

    @app.get("/health")
    def health():
        return {
            "status": "healthy",
            "version": APP_VERSION,
        }

    @app.get("/ready")
    def ready():
        return {
            "status": "ready",
            "version": APP_VERSION,
        }

    @app.get("/version")
    def version():
        return {
            "application": "flask-devops-api",
            "version": APP_VERSION,
        }

    return app
