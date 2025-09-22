from datetime import datetime
from sqlalchemy import func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.dbconfig import Base
from app.enums.estado import Estado


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado: Mapped[Estado] = mapped_column(
        SQLAlchemyEnum(Estado), default=Estado.HABILITADO, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )
