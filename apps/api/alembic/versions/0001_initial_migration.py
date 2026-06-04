"""Initial migration
Revision ID: 0001
"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "games",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("external_id", sa.BigInteger, unique=True, nullable=False),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("title_hash", sa.Text, nullable=False),
        sa.Column("image", sa.Text, nullable=False),
        sa.Column("category", sa.Text, nullable=False),
        sa.Column("tags", sa.ARRAY(sa.Text), nullable=True),
        sa.Column("embedding", Vector(1536), nullable=False),
        sa.Column("processed", sa.Boolean, server_default=sa.text("false"), nullable=False),
        sa.Column("reprocess_needed", sa.Boolean, server_default=sa.text("false"), nullable=False),
        sa.Column("last_synced_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column("processed_at", sa.TIMESTAMP(timezone=True)),
    )
    op.create_table(
        "sync_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("triggered_by", sa.Text, nullable=False),
        sa.Column("new_games", sa.Integer, server_default="0"),
        sa.Column("updated_games", sa.Integer, server_default="0"),
        sa.Column("queue_total", sa.Integer, server_default="0"),
        sa.Column("status", sa.Text, server_default="running"),
    )

    op.execute("CREATE INDEX ON games USING hnsw (embedding vector_cosine_ops)")
    op.execute("CREATE INDEX ON games (processed)")
    op.execute("CREATE INDEX ON games (external_id)")
    op.execute("CREATE INDEX ON games (category)")
    op.execute("CREATE INDEX ON games USING gin (tags)")

def downgrade() -> None:
    op.drop_table("sync_logs")
    op.drop_table("games")
    op.execute("DROP EXTENSION IF EXISTS vector")
