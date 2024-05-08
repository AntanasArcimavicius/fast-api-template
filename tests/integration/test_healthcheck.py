from unittest.mock import patch
from fastapi.testclient import TestClient

from payments_app.main import app

client = TestClient(app)


def test_healthcheck_success():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


@patch("payments_app.adapters.database.get_db", side_effect=Exception("Database error"))
def test_healthcheck_db_error(_):
    response = client.get("/healthcheck")
    assert response.status_code == 500
    assert "database" in response.json() and response.json()["database"] == "Failure"
