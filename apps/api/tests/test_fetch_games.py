import ast

from scripts.fetch_games import collect_game_data, collect_game_images
from config import config_settings

def test_collect_game_data(mocker):
    """
    Verify that game data collection returns accurate values.
    """
    games_page_1 = ast.literal_eval(config_settings.games_page_1)
    games_page_2 = ast.literal_eval(config_settings.games_page_2)
    queries = config_settings.queries
    
    mocker.patch("scripts.fetch_games.time.sleep")
    mock_get = mocker.patch("scripts.fetch_games.fetch_game_data")
    mock_get.side_effect = [games_page_1, games_page_2]

    games = collect_game_data(queries=queries, games_count=10000)

    assert len(games) == 3
    assert games[0]["external_id"] == 1
    assert games[0]["title"] == "Test Game Title"
    assert games[0]["player_count"] == 10000
    assert games[0]["image"] == ""
    assert games[0]["url"] == "https://www.roblox.com/test-url"
    assert games[1]["external_id"] == 2
    assert games[1]["title"] == "Test Game Title 2"
    assert games[1]["player_count"] == 9000
    assert games[1]["image"] == ""
    assert games[1]["url"] == "https://www.roblox.com/test-url-2"
    assert games[2]["external_id"] == 3
    assert games[2]["title"] == "Test Game Title 3"
    assert games[2]["player_count"] == 8000
    assert games[2]["image"] == ""
    assert games[2]["url"] == "https://www.roblox.com/test-url-3"

def test_collect_game_images(mocker):
    """
    Verify that game image collection returns accurate values.
    """
    images = ast.literal_eval(config_settings.images)
    
    games = [
        {"external_id": 1, "title": "Test Game Title", "player_count": 10000, "image": "", "url": "https://www.roblox.com/test-url"},
        {"external_id": 2, "title": "Test Game Title 2", "player_count": 9000, "image": "", "url": "https://www.roblox.com/test-url-2"},
        {"external_id": 3, "title": "Test Game Title 3", "player_count": 8000, "image": "", "url": "https://www.roblox.com/test-url-3"},
    ]
    mocker.patch("scripts.fetch_games.fetch_game_images", return_value=images)
    mocker.patch("scripts.fetch_games.time.sleep")

    games_images = collect_game_images(games)

    assert games_images[0]["image"] == "image"
    assert games_images[1]["image"] == "image-2"
    assert games_images[2]["image"] == "image-3"
