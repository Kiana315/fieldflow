
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.completion_record import CompletionRecord
from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base


class WorkOrderStatus(str, Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    customer_phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    service_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[WorkOrderStatus] = mapped_column(
        SQLEnum(
            WorkOrderStatus,
            name="work_order_status",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        default=WorkOrderStatus.NEW,
        server_default=text("'new'"),
        nullable=False,
    )

    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    creator: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    assignee: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[assigned_to_id],
    )

    completion_records: Mapped[list["CompletionRecord"]] = relationship(
        "CompletionRecord",
        back_populates="work_order",
    )