import os
import time

from flask import Flask, Response, g, request
from prometheus_client import (
     CONTENT_TYPE_LATEST,
     Counter,
     Histogram,
     generate_latest,
)

APP_VERSION = "1.0.0"

REQUEST_COUNT = Counter(
    "flask_api_requests_total",
    "Total number of requests received by the Flask API",
    ["endpoint", "method", "status"],
)

REQUEST_LATENCY = Histogram(
    "flask_api_request_duration_seconds",
    "Request latency in seconds",
    ["endpoint"],
)

def create_app():
    app = Flask(__name__)

    @app.before_request
    def track_request():
        g.request_start_time = time.perf_counter()
        

    @app.after_request
    def track_metrics(response):
        request_latency = time.perf_counter() - g.request_start_time

        REQUEST_COUNT.labels(
            endpoint=request.path,
            method=request.method,
            status=str(response.status_code),
        ).inc()

        REQUEST_LATENCY.labels(
            endpoint=request.path,
        ).observe(request_latency)

        return response

    @app.get("/")
    def home():
        return {
            "application": "flask-devops-api",
            "version": APP_VERSION,
            "environment": os.getenv("APP_ENV", "production"),
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

    @app.get("/metrics")
    def metrics():
        return Response(
            generate_latest(),
            mimetype=CONTENT_TYPE_LATEST,
        )
    

    return app
