import pytest


def test_showSummary_with_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200


def test_showSummary_with_invalid_email(client):
    response = client.post("/showSummary", data={"email": "invalid@example.com"})
    assert response.status_code == 401


if __name__ == "__main__":
    pytest.main()
