from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ImportJob(Base):   # this table is used to track the status of import jobs
    __tablename__ = "import_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
        index=True,
    )

    total_records: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    processed_records: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    valid_records: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    invalid_records: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    imported_records: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    errors = relationship(
        "ImportError",
        back_populates="import_job", 
        cascade="all, delete-orphan",
    )


class ImportError(Base):
    __tablename__ = "import_errors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    import_job_id: Mapped[int] = mapped_column(
        ForeignKey("import_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    row_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    errors: Mapped[dict] = mapped_column(
        JSON,        # jason is for storing multiple errors in a dictionary for a single row
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    import_job = relationship(
        "ImportJob",
        back_populates="errors",
    )