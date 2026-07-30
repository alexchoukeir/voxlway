from sqlalchemy import select

from services.sync import run
from models import Game

def test_add_games(get_db, mocker):
    """
    Verify that games are correctly added and that the saved game data is accurate.
    """
    games = {
        "games": [
            {
                "external_id": 1, 
                "title": "Test Title", 
                "player_count": 10000, 
                "image": "test-image", 
                "url": "test-url"
            },
            {
                "external_id": 2, 
                "title": "Test Title 2", 
                "player_count": 11000, 
                "image": "test-image-2", 
                "url": "test-url-2"
            }
        ]
    }
    mocker.patch("services.sync.SessionLocal", return_value=get_db)
    mocker.patch("services.sync.fetch_game_data", return_value=games)
    mocker.patch("services.sync.send_batch_messages")

    run("test")

    data = get_db.execute(select(Game).order_by(Game.external_id)).scalars().all()

    assert len(data) == 2

    assert data[0].external_id == 1
    assert data[0].title == "Test Title"
    assert data[0].player_count == 10000
    assert data[0].image == "test-image"
    assert data[0].url == "test-url"

    assert data[1].external_id == 2
    assert data[1].title == "Test Title 2"
    assert data[1].player_count == 11000
    assert data[1].image == "test-image-2"
    assert data[1].url == "test-url-2"
