from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_ready():
    app = create_app()
    client = app.test_client()

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json["status"] == "ready"


def test_version():
    app = create_app()
    client = app.test_client()

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json["version"] == "1.0.0"
