import pytest
import server

def test_purchasePlaces_with_valid_data(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 5
    }
    # Get the points club and the competition places before purchase
    initial_numberOfPlaces = int(server.competitions[0]['numberOfPlaces'])
    initial_clubPoints = int(server.clubs[0]['points'])

    response = client.post('/purchasePlaces/', data=data)

    # Verify that points and places are deducted
    remaining_places = initial_numberOfPlaces - 5
    remaining_points = initial_clubPoints - 5

    assert response.status_code == 200
    assert server.competitions[0]['numberOfPlaces'] == remaining_places
    assert server.clubs[0]['points'] == remaining_points

def test_purchasePlaces_with_invalid_competition(client):
    data = {
        'competition': 'invalid_competition',
        'club': 'Simply Lift',
        'places': 5
    }
    response = client.post('/purchasePlaces/', data=data)
    assert response.status_code == 404
    assert b"Invalid competition" in response.data

def test_purchasePlaces_with_invalid_club(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'invalid_club',
        'places': 5
    }
    response = client.post('/purchasePlaces/', data=data)
    assert response.status_code == 404
    assert b"Invalid club" in response.data

def test_purchasePlaces_with_invalid_number_of_places(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 15
    }
    response = client.post('/purchasePlaces/', data=data)
    assert response.status_code == 200
    assert b'Invalid number of places' in response.data

if __name__ == '__main__':
    pytest.main()