from datetime import datetime
from uuid import UUID, uuid4
from pgvector.sqlalchemy import Vector

from sqlalchemy import DateTime, String, BigInteger, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Document(Base):
  __tablename__ = "documents"

  id: Mapped[UUID] = mapped_column(
    primary_key= True,
    default=uuid4
  )

  filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

  file_path: Mapped[str] = mapped_column(
      String(500),
      nullable=False
  )

  file_size: Mapped[int] = mapped_column(
      BigInteger,
      nullable=False
  )

  status: Mapped[str] = mapped_column(
      String(50),
      nullable=False,
      default="uploaded"
  )

  created_at: Mapped[datetime] = mapped_column(
      DateTime,
      default=datetime.utcnow,
      nullable=False
  )

class DocumentChunk(Base):
  __tablename__ = "document_chunks"

  id: Mapped[UUID] = mapped_column(
    primary_key=True,
    default=uuid4
  )

  document_id: Mapped[UUID] = mapped_column(
    ForeignKey("documents.id"),
    nullable=False
  )

  chunk_index: Mapped[int] = mapped_column(
      Integer,
      nullable=False
  )

  content: Mapped[str] = mapped_column(
      Text,
      nullable=False
  )

  page_number: Mapped[int] = mapped_column(
      Integer,
      nullable=False
  )

  embedding: Mapped[list[float] | None] = mapped_column(
    Vector(3072),
    nullable=True
  )