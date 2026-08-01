from sqlalchemy import func, select

from services.sync import run
from models import Game

GAMES = {
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

def test_add_games(get_db, mocker):
    """
    Verify that games are correctly added and that the saved game data is accurate.
    """
    mocker.patch("services.sync.SessionLocal", return_value=get_db)
    mocker.patch("services.sync.fetch_game_data", return_value=GAMES)
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

def test_duplicates_data_unchanged(get_db, mocker):
    """
    Verify that duplicate games are not added and that the existing game data remains unchanged.
    """

    get_db.add(Game(external_id=2, title="Test Title 2", player_count=11000, image="test-image-2", url="test-url-2"))
    get_db.commit()
    
    mocker.patch("services.sync.SessionLocal", return_value=get_db)
    mocker.patch("services.sync.fetch_game_data", return_value=GAMES)
    mocker.patch("services.sync.send_batch_messages")

    run("test")

    assert get_db.scalar(select(func.count(Game.id))) == 2
    
    assert get_db.scalar(select(Game).where(Game.title == "Test Title")) is not None

def test_duplicates_data_changed(get_db, mocker):
    """
    Verify that duplicate games are not added and that the existing game data is updated if it has changed.
    """

    game = Game(external_id=2, title="Test Title 2 Old", player_count=9000, image="test-image-2-old", url="test-url-2-old")
    get_db.add(game)
    get_db.commit()

    game_id = game.id

    mocker.patch("services.sync.SessionLocal", return_value=get_db)
    mocker.patch("services.sync.fetch_game_data", return_value=GAMES)
    mocker.patch("services.sync.send_batch_messages")

    run("test")

    assert get_db.scalar(select(func.count(Game.id))) == 2

    assert get_db.scalar(select(Game).where(Game.title == "Test Title")) is not None

    assert get_db.scalar(select(Game.external_id).where(Game.id == game_id)) == 2
    assert get_db.scalar(select(Game.title).where(Game.id == game_id)) == "Test Title 2"
    assert get_db.scalar(select(Game.player_count).where(Game.id == game_id)) == 11000
    assert get_db.scalar(select(Game.image).where(Game.id == game_id)) == "test-image-2"
    assert get_db.scalar(select(Game.url).where(Game.id == game_id)) == "test-url-2"
