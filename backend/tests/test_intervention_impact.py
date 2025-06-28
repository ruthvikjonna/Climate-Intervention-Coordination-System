import uuid
from datetime import datetime, timezone
from app.models.climate_grid_cell import ClimateGridCell
from app.models.operator import Operator
from app.models.intervention import Intervention

def test_create_and_get_intervention_impact(client, db):
    # Create a grid cell using ORM
    grid_cell_id = uuid.uuid4()
    cell = ClimateGridCell(
        id=grid_cell_id,
        latitude=0.0,
        longitude=0.0,
        grid_resolution="1km",
        measurement_timestamp=datetime.now(timezone.utc),
        co2_ppm=400,
        temperature_celsius=20,
        biomass_index=1,
        data_source="NASA",
        source_metadata={},
        created_at=datetime.now(timezone.utc)
    )
    db.add(cell)
    # Create an operator using ORM
    operator_id = uuid.uuid4()
    operator = Operator(
        id=operator_id,
        name="Test Operator",
        organization_type="research",
        email="test@example.com",
        api_key="key123",
        permissions={},
        created_at=datetime.now(timezone.utc)
    )
    db.add(operator)
    # Create an intervention using ORM
    intervention_id = uuid.uuid4()
    intervention = Intervention(
        id=intervention_id,
        operator_id=operator_id,
        grid_cell_id=grid_cell_id,
        name="Test Intervention",
        intervention_type="SRM",
        status="active",
        latitude=0.0,
        longitude=0.0,
        region_name="Test Region",
        scale_amount=100,
        scale_unit="tonnes_co2",
        cost_usd=1000,
        start_date=datetime.now(timezone.utc).date(),
        end_date=datetime.now(timezone.utc).date(),
        duration_months=12,
        deployment_data={},
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        description="desc"
    )
    db.add(intervention)
    db.commit()

    payload = {
        "intervention_id": str(intervention_id),
        "grid_cell_id": str(grid_cell_id),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature_change": 1.5,
        "effectiveness_score": 0.9
    }
    response = client.post("/api/v1/intervention-impacts/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["temperature_change"] == 1.5

    # Get
    response = client.get(f"/api/v1/intervention-impacts/{data['id']}")
    assert response.status_code == 200
    assert response.json()["effectiveness_score"] == 0.9 