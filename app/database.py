from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/chatpdf"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
  bind=engine,
  autoflush=False,
  autocommit=False
)

class Base(DeclarativeBase):
  pass
