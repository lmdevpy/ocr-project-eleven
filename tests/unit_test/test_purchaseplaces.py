import pytest

def test_purchasePlaces_with_valid_data(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 5
    }
    response = client.post('/purchasePlaces/Simply%20Lift', data=data)
    assert response.status_code == 200

def test_purchasePlaces_with_invalid_competition(client):
    data = {
        'competition': 'invalid_competition',
        'club': 'Simply Lift',
        'places': 5
    }
    response = client.post('/purchasePlaces/Simply%20Lift', data=data)
    assert response.status_code == 404

def test_purchasePlaces_with_invalid_club(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'invalid_club',
        'places': 5
    }
    response = client.post('/purchasePlaces/invalid_club', data=data)
    assert response.status_code == 404

def test_purchasePlaces_with_invalid_number_of_places(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 15
    }
    response = client.post('/purchasePlaces/Simply%20Lift', data=data)
    assert response.status_code == 200  # Adjust the status code based on your application logic
    with client.session_transaction() as session:
        flash_messages = dict(session['_flashes'])
        assert 'Invalid number of places' in flash_messages['message']

if __name__ == '__main__':
    pytest.main()