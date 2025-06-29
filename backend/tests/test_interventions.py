import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_intervention(supabase):
    """Test creating a new intervention"""
    intervention_data = {
        "operator_id": str(uuid4()),
        "grid_cell_id": str(uuid4()),
        "name": "Test Biochar Project",
        "description": "A test biochar intervention",
        "intervention_type": "biochar",
        "status": "planned",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "region_name": "New York",
        "scale_amount": 1000.0,
        "scale_unit": "tonnes_co2",
        "cost_usd": 50000.0,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "duration_months": 12
    }
    
    response = client.post("/api/v1/interventions/", json=intervention_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == intervention_data["name"]
    assert data["intervention_type"] == intervention_data["intervention_type"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_interventions(supabase):
    """Test getting list of interventions"""
    response = client.get("/api/v1/interventions/")
    assert response.status_code == 200
    
    data = response.json()
    assert "interventions" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data


def test_get_intervention_by_id(supabase):
    """Test getting a specific intervention by ID"""
    # First create an intervention
    intervention_data = {
        "operator_id": str(uuid4()),
        "grid_cell_id": str(uuid4()),
        "name": "Test DAC Project",
        "description": "A test DAC intervention",
        "intervention_type": "DAC",
        "status": "active",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "region_name": "Los Angeles",
        "scale_amount": 500.0,
        "scale_unit": "tonnes_co2",
        "cost_usd": 25000.0
    }
    
    create_response = client.post("/api/v1/interventions/", json=intervention_data)
    assert create_response.status_code == 201
    
    intervention_id = create_response.json()["id"]
    
    # Then get it by ID
    response = client.get(f"/api/v1/interventions/{intervention_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == intervention_id
    assert data["name"] == intervention_data["name"]


def test_update_intervention(supabase):
    """Test updating an intervention"""
    # First create an intervention
    intervention_data = {
        "operator_id": str(uuid4()),
        "grid_cell_id": str(uuid4()),
        "name": "Test Afforestation Project",
        "description": "A test afforestation intervention",
        "intervention_type": "afforestation",
        "status": "planned",
        "latitude": 41.8781,
        "longitude": -87.6298,
        "region_name": "Chicago",
        "scale_amount": 100.0,
        "scale_unit": "hectares",
        "cost_usd": 10000.0
    }
    
    create_response = client.post("/api/v1/interventions/", json=intervention_data)
    assert create_response.status_code == 201
    
    intervention_id = create_response.json()["id"]
    
    # Then update it
    update_data = {
        "status": "active",
        "description": "Updated description"
    }
    
    response = client.put(f"/api/v1/interventions/{intervention_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "active"
    assert data["description"] == "Updated description"


def test_delete_intervention(supabase):
    """Test deleting an intervention"""
    # First create an intervention
    intervention_data = {
        "operator_id": str(uuid4()),
        "grid_cell_id": str(uuid4()),
        "name": "Test SRM Project",
        "description": "A test SRM intervention",
        "intervention_type": "SRM",
        "status": "planned",
        "latitude": 29.7604,
        "longitude": -95.3698,
        "region_name": "Houston",
        "scale_amount": 50.0,
        "scale_unit": "kg_aerosol",
        "cost_usd": 75000.0
    }
    
    create_response = client.post("/api/v1/interventions/", json=intervention_data)
    assert create_response.status_code == 201
    
    intervention_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/api/v1/interventions/{intervention_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/interventions/{intervention_id}")
    assert get_response.status_code == 404 