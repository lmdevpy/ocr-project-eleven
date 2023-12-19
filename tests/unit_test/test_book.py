import pytest

def test_book_with_valid_data(client):
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert response.status_code == 200

def test_book_with_finished_competition(client):
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert response.status_code == 200
    assert b"competition is finished" in response.data

def test_book_with_invalid_club(client):
    response = client.get('/book/Fall%20Classic/invalid_club')
    assert response.status_code == 404
    assert b"club not found" in response.data

def test_book_with_invalid_competition(client):
    response = client.get('/book/invalid_competition/Simply%20Lift')
    assert response.status_code == 404
    assert b"competition not found" in response.data

if __name__ == '__main__':
    pytest.main()