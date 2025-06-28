from sqlalchemy import Column, String, JSON, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    organization_type = Column(String, nullable=False)  # "startup", "government", "NGO", "research"
    email = Column(String, unique=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False)  # for data access
    permissions = Column(JSON)  # what data they can access
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    interventions = relationship("Intervention", back_populates="operator")
    optimization_results = relationship("OptimizationResult", back_populates="operator")

    # Indexes for performance
    __table_args__ = (
        Index('idx_operators_api_key', 'api_key'),
        Index('idx_operators_email', 'email'),
        Index('idx_operators_org_type', 'organization_type'),
    ) 