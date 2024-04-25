from src.database.config import Base
from sqlalchemy import ForeignKey, text, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    id_tg: Mapped[int] = mapped_column(nullable=False, unique=True)
    subscription: Mapped[int] = mapped_column(ForeignKey('site.id'), nullable=True)
    pagination: Mapped[int] = mapped_column(default=5, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), nullable=False
    )


