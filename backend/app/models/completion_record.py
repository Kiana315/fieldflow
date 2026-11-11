
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.work_order import WorkOrder


class CompletionRecord(Base):
    __tablename__ = "work_order_completion_records"

    id: Mapped[int] = mapped_column(primary_key=True)

    work_order_id: Mapped[int] = mapped_column(
        ForeignKey("work_orders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    technician_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    notes: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    work_order: Mapped["WorkOrder"] = relationship(
        "WorkOrder",
        back_populates="completion_records",
    )

    technician: Mapped["User"] = relationship(
        "User",
        foreign_keys=[technician_id],
    )

    __table_args__ = (
        CheckConstraint(
            "length(btrim(notes)) > 0",
            name="ck_completion_notes_not_blank",
        ),
    )