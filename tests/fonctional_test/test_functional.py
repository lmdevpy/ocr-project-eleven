import pytest
import server


def test_login_and_reserve_points(client, fixture_loadClubs, fixture_loadCompetitions):
    login_response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert login_response.status_code == 200

    book_response = client.get(f"/book/Paris%20World/Simply%20Lift")
    assert book_response.status_code == 200

    remaining_competitions_places = int(server.competitions[0]['numberOfPlaces']) - 5
    remaining_club_points = int(server.clubs[0]['points']) - 5
    purchase_response = client.post('/purchasePlaces/', data={'competition': 'Paris World',
                                                             'club': 'Simply Lift',
                                                             'places': 5})
    assert book_response.status_code == 200
    assert server.clubs[0]['points'] == remaining_club_points
    assert server.competitions[0]['numberOfPlaces'] == remaining_competitions_places