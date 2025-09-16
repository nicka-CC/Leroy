from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Database URL: default to SQLite file in project, can be overridden by env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Example: postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME
    "postgresql+psycopg2://postgres:nikita12345@localhost:5432/lerom",
)

# PostgreSQL doesn't require special connect args like SQLite
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables for all metadata models."""
    # Import models so that Base.metadata is populated
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


