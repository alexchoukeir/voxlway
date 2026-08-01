import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from database import Base

@pytest.fixture
def get_db():
    """
    Hands a database session for testing.

    Yields:
        Session: A SQLAlchemy session object.
    """
    host = os.environ['DB_HOST']
    password = os.environ['DB_PASSWORD']
    name = os.environ['DB_NAME']
    user = os.environ['DB_USER']

    url = f"postgresql://{user}:{password}@{host}/{name}"

    engine = create_engine(url)
    connection = engine.connect()

    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    connection.commit()

    Base.metadata.create_all(engine)
    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
