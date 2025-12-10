import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./image_import.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# engine with pre-ping so stale/closed connections are detected and replaced
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,            # check connection before using from pool
    pool_size=5,                   # adjust to your deploy size
    max_overflow=10,               # temporary connections beyond pool_size
    pool_timeout=30,               # seconds to wait for connection from pool
    connect_args={"sslmode": "require"},  # ensure SSL for providers that need it
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ⬇⬇⬇ ADD THIS PART (MISSING) ⬇⬇⬇
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
