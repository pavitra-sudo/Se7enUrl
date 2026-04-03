
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from api.v1.config.db_url import DATABASE_URL

DATABASE_URL = DATABASE_URL

# Engine
engine = create_engine(
    DATABASE_URL,  # type: ignore
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base classes
ShortURLBase = declarative_base()



        