from pydantic import BaseModel

class Games(BaseModel):
    id: int
    external_id: int
    title: str
    player_count: int
    url: str
    image: str
    category: str | None = None
    tags: list[str] | None = None
    similarity: float
