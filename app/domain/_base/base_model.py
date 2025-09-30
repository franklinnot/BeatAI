from datetime import datetime
import pytz
from sqlalchemy import func, Enum as SQLAlchemyEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.dbconfig import Base
from app.enums.estado import Estado

# zona horaria de Perú
PERU_TIMEZONE = pytz.timezone("America/Lima")


def get_peru_time() -> datetime:
    return datetime.now(PERU_TIMEZONE)


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado: Mapped[Estado] = mapped_column(
        SQLAlchemyEnum(Estado), default=Estado.HABILITADO, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_peru_time, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_peru_time,
        onupdate=get_peru_time,
        nullable=False,
    )
