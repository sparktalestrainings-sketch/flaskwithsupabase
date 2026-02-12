import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_URL = os.getenv("DATABASE_URL")  # for PostgreSQL on Railway
if not DB_URL:
    # fallback to local SQLite for dev/testing
    DB_URL = "sqlite:///chat_history.db"

engine = create_engine(DATABASE_URL,pool_pre_ping=True, echo=True, future=True)

#SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
SessionLocal = sessionmaker(bind=engine)