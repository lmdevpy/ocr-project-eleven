import pytest

def test_book_with_valid_data(client):
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert response.status_code == 200

def test_book_with_invalid_club(client):
    response = client.get('/book/Fall%20Classic/invalid_club')
    assert response.status_code == 404

def test_book_with_invalid_competition(client):
    response = client.get('/book/invalid_competition/Simply%20Lift')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main()