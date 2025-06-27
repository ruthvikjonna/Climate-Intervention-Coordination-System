import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

# Sample intervention data
test_interventions = [
    {
        "name": "Carbon Engineering DAC Plant - Squamish",
        "description": "Direct Air Capture facility in British Columbia",
        "intervention_type": "DAC",
        "location_lat": 49.7016,
        "location_lon": -123.1558,
        "deployment_date": "2023-06-15T00:00:00",
        "capacity_tonnes_co2": 1000000,
        "status": "operational",
        "operator": "Carbon Engineering",
        "cost_per_tonne": 94.0,
        "technology_readiness_level": 8,
        "verification_method": "ISO 14064-2",
        "expected_lifetime_years": 30
    },
    {
        "name": "Climeworks Orca Plant",
        "description": "World's largest direct air capture plant",
        "intervention_type": "DAC",
        "location_lat": 64.9631,
        "location_lon": -19.0208,
        "deployment_date": "2021-09-08T00:00:00",
        "capacity_tonnes_co2": 4000,
        "status": "operational",
        "operator": "Climeworks",
        "cost_per_tonne": 600.0,
        "technology_readiness_level": 7,
        "verification_method": "ISO 14064-2",
        "expected_lifetime_years": 25
    },
    {
        "name": "Pacific Biochar Facility",
        "description": "Biochar production from forest waste",
        "intervention_type": "biochar",
        "location_lat": 47.6062,
        "location_lon": -122.3321,
        "deployment_date": "2022-03-20T00:00:00",
        "capacity_tonnes_co2": 50000,
        "status": "operational",
        "operator": "Pacific Biochar",
        "cost_per_tonne": 150.0,
        "technology_readiness_level": 8,
        "verification_method": "Puro.earth",
        "expected_lifetime_years": 100
    },
    {
        "name": "Amazon Reforestation Project",
        "description": "Large-scale reforestation in the Amazon",
        "intervention_type": "reforestation",
        "location_lat": -3.4653,
        "location_lon": -58.3804,
        "deployment_date": "2020-01-15T00:00:00",
        "capacity_tonnes_co2": 250000,
        "status": "operational",
        "operator": "Amazon Conservation",
        "cost_per_tonne": 25.0,
        "technology_readiness_level": 9,
        "verification_method": "Verified Carbon Standard",
        "expected_lifetime_years": 50
    },
    {
        "name": "Ocean Fertilization Experiment",
        "description": "Iron fertilization to stimulate phytoplankton growth",
        "intervention_type": "ocean_fertilization",
        "location_lat": -45.0,
        "location_lon": 172.0,
        "deployment_date": "2023-01-10T00:00:00",
        "capacity_tonnes_co2": 10000,
        "status": "experimental",
        "operator": "Ocean Carbon Institute",
        "cost_per_tonne": 75.0,
        "technology_readiness_level": 4,
        "verification_method": "Ocean Carbon Verification",
        "expected_lifetime_years": 5
    },
    {
        "name": "Enhanced Weathering Project - Iceland",
        "description": "Basalt weathering to capture CO2",
        "intervention_type": "enhanced_weathering",
        "location_lat": 64.9631,
        "location_lon": -19.0208,
        "deployment_date": "2022-08-30T00:00:00",
        "capacity_tonnes_co2": 15000,
        "status": "operational",
        "operator": "Carbfix",
        "cost_per_tonne": 25.0,
        "technology_readiness_level": 7,
        "verification_method": "ISO 14064-2",
        "expected_lifetime_years": 1000
    }
]

def add_test_data():
    """Add test interventions to the database"""
    print("Adding test interventions...")
    
    for i, intervention in enumerate(test_interventions, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/interventions/",
                json=intervention,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                print(f"✅ Added intervention {i}: {intervention['name']}")
            else:
                print(f"❌ Failed to add intervention {i}: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to the API. Make sure the backend server is running on http://localhost:8000")
            return
        except Exception as e:
            print(f"❌ Error adding intervention {i}: {e}")

def check_existing_data():
    """Check if there are already interventions in the database"""
    try:
        response = requests.get(f"{BASE_URL}/interventions/")
        if response.status_code == 200:
            data = response.json()
            if data.get('interventions') and len(data['interventions']) > 0:
                print(f"Found {len(data['interventions'])} existing interventions")
                return True
    except:
        pass
    return False

if __name__ == "__main__":
    print("🌍 Planetary Temperature Control Platform - Test Data Generator")
    print("=" * 60)
    
    # Check if data already exists
    if check_existing_data():
        print("⚠️  Data already exists. Skipping test data creation.")
    else:
        add_test_data()
        print("\n🎉 Test data creation complete!")
        print("You can now view the dashboard at: http://localhost:3000")
        print("API documentation at: http://localhost:8000/docs") 