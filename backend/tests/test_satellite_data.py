import uuid
from datetime import datetime, timezone
from app.models.climate_grid_cell import ClimateGridCell

def test_create_and_get_satellite_data(client, db):
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
    db.commit()

    payload = {
        "grid_cell_id": str(grid_cell_id),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": 20.5,
        "satellite_id": "SAT-001"
    }
    response = client.post("/api/v1/satellite-data/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["temperature"] == 20.5

    # Get
    response = client.get(f"/api/v1/satellite-data/{data['id']}")
    assert response.status_code == 200
    assert response.json()["satellite_id"] == "SAT-001" 