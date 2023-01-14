import os
import uuid

from databases import Database
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
    ),
    Column(
        "idempotency_id",
        UUID(as_uuid=True),
        index=True,
        default=str(uuid.uuid4()),
        unique=True,
    ),
    Column("type", String, nullable=False),
    Column("side", String, nullable=False),
    Column("status", String, nullable=False),
    Column("instrument", String, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("limit_price_cents", Integer, nullable=True),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now()),
)

# databases query builder
database = Database(DATABASE_URL)
