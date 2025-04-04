import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Detect environment
if os.environ.get('HEROKU'):
    # Heroku PostgreSQL configuration
    SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']
    # Fix for SQLAlchemy 1.4+
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # Local SQLite configuration
    SQLALCHEMY_DATABASE_URL = "sqlite:///./transactions.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()