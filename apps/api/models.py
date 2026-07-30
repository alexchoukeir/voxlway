from sqlalchemy import Text, Integer, BigInteger, ARRAY, Boolean, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pgvector.sqlalchemy import Vector
from datetime import datetime

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    title: Mapped[str] = mapped_column(Text)
    player_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    url: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    embedding: Mapped[Vector | None] = mapped_column(Vector(1536))
    processed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    reprocess_needed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    last_synced_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    processed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    triggered_by: Mapped[str] = mapped_column(Text)
    new_games: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    updated_games: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    queue_total: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[str] = mapped_column(Text, default="running", server_default="running")
