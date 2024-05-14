from unittest.mock import patch
from fastapi.testclient import TestClient

from payments_app.main import app

client = TestClient(app)


def test_healthcheck_success():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "database": "OK"}
