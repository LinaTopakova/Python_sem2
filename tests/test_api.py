from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_model_info() -> None:
    resp = client.get("/model-info")
    assert resp.status_code == 200
    data = resp.json()
    assert "name" in data
