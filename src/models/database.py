# in models/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from the project's .env file
load_dotenv()

# --- Database Connection Setup ---

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")

# Create the SQLAlchemy engine. This is the core interface to the database.
engine = create_engine(DATABASE_URL)

# Create a sessionmaker, which will serve as a factory for new Session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Declarative Base ---

# This is the central Base class that all your models will inherit from.
Base = declarative_base()


# --- Session Context Manager ---

def get_session():
    """
    Context manager for database sessions.
    Ensures proper cleanup of database connections.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()