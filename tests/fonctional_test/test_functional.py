import pytest
import server


def test_login_and_reserve_points(client, fixture_loadClubs, fixture_loadCompetitions):
    login_response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert login_response.status_code == 200

    book_response = client.get(f"/book/Paris%20World/Simply%20Lift")
    assert book_response.status_code == 200

    remaining_competitions_places = int(server.competitions[0]["numberOfPlaces"]) - 5
    remaining_club_points = int(server.clubs[0]["points"]) - 5
    purchase_response = client.post(
        "/purchasePlaces/",
        data={"competition": "Paris World", "club": "Simply Lift", "places": 5},
    )
    assert purchase_response.status_code == 200
    assert server.clubs[0]["points"] == remaining_club_points
    assert server.competitions[0]["numberOfPlaces"] == remaining_competitions_places


def test_login_and_purchase_two_times(
    client, fixture_loadClubs, fixture_loadCompetitions
):
    login_response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert login_response.status_code == 200

    book_response = client.get(f"/book/Paris%20World/Simply%20Lift")
    assert book_response.status_code == 200

    purchase_response = client.post(
        "/purchasePlaces/",
        data={"competition": "Paris World", "club": "Simply Lift", "places": 5},
    )
    assert purchase_response.status_code == 200

    other_book_response = client.get(f"/book/London%20Big%20Tour/Simply%20Lift")
    assert other_book_response.status_code == 200

    other_purchase_response = client.post(
        "/purchasePlaces/",
        data={"competition": "London Big Tour", "club": "Simply Lift", "places": 7},
    )
    assert other_purchase_response.status_code == 200


def test_purchase_and_updated_board_points(
    client, fixture_loadClubs, fixture_loadCompetitions
):
    response = client.get("/displayPointsBoard/")
    board_before_purchase = response.data
    assert response.status_code == 200

    book_response = client.get(f"/book/Paris%20World/Simply%20Lift")
    assert book_response.status_code == 200

    purchase_response = client.post(
        "/purchasePlaces/",
        data={"competition": "Paris World", "club": "Simply Lift", "places": 5},
    )
    assert purchase_response.status_code == 200

    second_response = client.get("/displayPointsBoard/")
    assert second_response.status_code == 200

    board_after_purchase = second_response.data
    assert board_before_purchase != board_after_purchase


# SE CONNECTER ACHETER DES PLACES PLUS QUE DE POINT DISPONIBLE ET VERIFIER QUE LE BOARD EST LE MEME
def test_purchase_invalid_points(client, fixture_loadClubs, fixture_loadCompetitions):
    response = client.get("/displayPointsBoard/")
    board_before_purchase = response.data
    assert response.status_code == 200

    book_response = client.get(f"/book/Paris%20World/Iron%20Temple")
    assert book_response.status_code == 200

    purchase_response = client.post(
        "/purchasePlaces/",
        data={"competition": "Paris World", "club": "Iron Temple", "places": 9},
    )
    assert purchase_response.status_code == 200
    assert b"Invalid number of places" in purchase_response.data
    second_response = client.get("/displayPointsBoard/")
    assert second_response.status_code == 200

    board_after_purchase = second_response.data
    assert board_before_purchase == board_after_purchase


if __name__ == "__main__":
    pytest.main()
