import uuid
from datetime import datetime, timezone
from app.models.climate_grid_cell import ClimateGridCell
from app.models.operator import Operator

def test_create_and_get_optimization_result(client, db):
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
        email="test2@example.com",
        api_key="key456",
        permissions={},
        created_at=datetime.now(timezone.utc)
    )
    db.add(operator)
    db.commit()

    payload = {
        "operator_id": str(operator_id),
        "grid_cell_id": str(grid_cell_id),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "optimization_type": "temperature",
        "algorithm": "genetic",
        "optimal_parameters": {"param1": 1.0},
        "status": "completed"
    }
    response = client.post("/api/v1/optimization-results/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["optimization_type"] == "temperature"

    # Get
    response = client.get(f"/api/v1/optimization-results/{data['id']}")
    assert response.status_code == 200
    assert response.json()["algorithm"] == "genetic" 