from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

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