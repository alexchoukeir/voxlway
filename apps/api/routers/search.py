from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.embeddings import async_generate_embedding
from models import Game
from schemas import Games
from limiter import limiter

router = APIRouter()

@router.get("/search")
@limiter.limit("8/hour")
async def search(
    request: Request,
    q: str = Query(..., description="The search query", min_length=1, max_length=150),
    db: AsyncSession = Depends(get_db)
) -> list[Games]:
    """
    Searches for games based on the provided query.
    """
    try:
        # Generate embedding for the query
        embedding = await async_generate_embedding(q.strip())
    except Exception as e:
        raise HTTPException(status_code=503, detail="Search service is currently unavailable. Please try again later.") from e

    # Calculate cosine similarity
    distance = Game.embedding.cosine_distance(embedding)
    similarity = 1 - distance

    # Query the database
    try:
        query = (
            select(Game, similarity.label("similarity"))
            .where(Game.processed)
            .where(similarity >= 0.65)
            .order_by(distance)
            .limit(24)
        )
        
        results = await db.execute(query)
        results = results.all()
    except Exception as e:
        raise HTTPException(status_code=503, detail="Search service is currently unavailable. Please try again later.") from e

    return [
        {
            "id": game.id,
            "external_id": game.external_id,
            "title": game.title,
            "player_count": game.player_count,
            "url": game.url,
            "image": game.image,
            "category": game.category,
            "tags": game.tags,
            "similarity": similarity
        }
        for game, similarity in results
    ]
