from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    intervention_type = Column(String, index=True)
    location_lat = Column(Float)
    location_lon = Column(Float)
    deployment_date = Column(DateTime, nullable=True)
    capacity_tonnes_co2 = Column(Float)
    status = Column(String, index=True)
    operator = Column(String, index=True)
    cost_per_tonne = Column(Float, nullable=True)
    technology_readiness_level = Column(Integer, nullable=True)
    verification_method = Column(String, nullable=True)
    expected_lifetime_years = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())