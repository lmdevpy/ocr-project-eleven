import pytest
import json
import server
from datetime import datetime
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def fixture_loadClubs(monkeypatch):
    def mock_loadClubs():
        with open("tests/test_clubs.json") as clubs:
            listOfClubs = json.load(clubs)["clubs"]
            return listOfClubs

    monkeypatch.setattr("server.clubs", mock_loadClubs())


@pytest.fixture
def fixture_loadCompetitions(monkeypatch):
    def mock_loadCompetitions():
        with open("tests/test_competitions.json") as comps:
            listOfCompetitions = json.load(comps)["competitions"]
            date_now = datetime.now()
            for competition in listOfCompetitions:
                competition["date"] = datetime.strptime(
                    competition["date"], "%Y-%m-%d %H:%M:%S"
                )
                competition["finished"] = competition["date"] < date_now
            return listOfCompetitions

    monkeypatch.setattr("server.competitions", mock_loadCompetitions())
