def test_create_and_get_data_source(client):
    payload = {
        "name": "Test Source",
        "source_type": "satellite",
        "provider": "NASA",
        "url": "https://nasa.gov/data",
        "is_active": True
    }
    response = client.post("/api/v1/data-sources/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Source"
    assert data["provider"] == "NASA"

    # Get by ID
    response = client.get(f"/api/v1/data-sources/{data['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Source" 