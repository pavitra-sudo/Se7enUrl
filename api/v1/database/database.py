
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from api.v1.config.db_url import DATABASE_URL

DATABASE_URL = DATABASE_URL

# Engine configuration depending on SQLite or PostgreSQL
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs["pool_size"] = 5
    engine_kwargs["max_overflow"] = 10

engine = create_engine(
    DATABASE_URL,  # type: ignore
    pool_pre_ping=True,
    **engine_kwargs
)

# Session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base classes
ShortURLBase = declarative_base()



        