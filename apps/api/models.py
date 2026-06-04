from sqlalchemy import Text, Integer, BigInteger, ARRAY, Boolean, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pgvector.sqlalchemy import Vector
from datetime import datetime

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    title_hash: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=True)
    embedding: Mapped[Vector] = mapped_column(Vector(1536), nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    reprocess_needed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    last_synced_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    processed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    triggered_by: Mapped[str] = mapped_column(Text, nullable=False)
    new_games: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    updated_games: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    queue_total: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[str] = mapped_column(Text, default="running", server_default="running")
