import datetime

from src.database.config import Base
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class News(Base):
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    link_to_news: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), nullable=False
    )
    id_site: Mapped[int] = mapped_column(ForeignKey('site.id'))


class Site(Base):
    __tablename__ = "site"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
