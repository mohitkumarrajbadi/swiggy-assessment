import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

MAX_RETRIES = 10
RETRY_DELAY = 2

def get_engine():
    # Use SQLite in-memory for testing if DATABASE_URL starts with sqlite or is missing
    is_sqlite = not DATABASE_URL or DATABASE_URL.startswith("sqlite")
    
    engine = create_engine(DATABASE_URL if DATABASE_URL else "sqlite:///:memory:")
    
    if is_sqlite:
        return engine

    for i in range(MAX_RETRIES):
        try:
            # Just try a quick connect to verify availability
            with engine.connect():
                print("Database connected")
            return engine
        except Exception:
            print(f"Database not ready, retrying... ({i+1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    
    raise Exception("Could not connect to database after several attempts")

engine = get_engine()
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()