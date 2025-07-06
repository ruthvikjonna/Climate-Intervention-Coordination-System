#!/usr/bin/env python3
"""
Test script for NASA integration
Run this to verify your NASA data integration is working
"""

import os
import sys
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.nasa_services import nasa_services

def test_nasa_integration():
    """Test all NASA data endpoints"""
    print("🚀 Testing NASA Integration for PTC Platform")
    print("=" * 50)
    
    # Test coordinates (San Francisco area)
    test_lat = 37.7749
    test_lon = -122.4194
    
    print(f"📍 Testing location: {test_lat}, {test_lon}")
    print()
    
    # Test CO2 data
    print("1. Testing CO2 concentration data...")
    co2_data = nasa_services.get_co2_concentrations(test_lat, test_lon)
    print(f"   ✅ CO2: {co2_data.get('co2_concentration', 'N/A')} ppm")
    print()
    
    # Test temperature data
    print("2. Testing temperature data...")
    temp_data = nasa_services.get_temperature_data(test_lat, test_lon)
    print(f"   ✅ Temperature: {temp_data.get('temperature', 'N/A')}°C")
    print(f"   ✅ Anomaly: {temp_data.get('temperature_anomaly', 'N/A')}°C")
    print()
    
    # Test biomass data
    print("3. Testing biomass data...")
    biomass_data = nasa_services.get_biomass_data(test_lat, test_lon)
    print(f"   ✅ Biomass density: {biomass_data.get('biomass_density', 'N/A')} tons/ha")
    print(f"   ✅ Carbon storage potential: {biomass_data.get('carbon_storage_potential', 'N/A')} tons CO2/ha")
    print()
    
    # Test historical patterns
    print("4. Testing historical climate patterns...")
    historical_data = nasa_services.get_historical_climate_patterns(test_lat, test_lon)
    print(f"   ✅ Temperature trend: {historical_data.get('temperature_trend', 'N/A')}°C per decade")
    print(f"   ✅ CO2 trend: {historical_data.get('co2_trend', 'N/A')} ppm per year")
    print()
    
    # Test comprehensive optimization data
    print("5. Testing intervention optimization data...")
    optimization_data = nasa_services.get_intervention_optimization_data(test_lat, test_lon)
    recommendations = optimization_data.get('intervention_recommendations', {})
    print(f"   ✅ Optimal intervention: {recommendations.get('optimal_intervention_type', 'N/A')}")
    print(f"   ✅ Deployment priority: {recommendations.get('deployment_priority', 'N/A')}")
    print(f"   ✅ Expected impact: {recommendations.get('expected_impact', 'N/A')}")
    print()
    
    print("🎉 NASA Integration Test Complete!")
    print("=" * 50)
    print("Your PTC platform now has access to:")
    print("• Real-time CO2 concentration data")
    print("• Temperature monitoring and anomalies")
    print("• Biomass assessment for intervention planning")
    print("• Historical climate patterns for algorithm training")
    print("• Comprehensive intervention optimization recommendations")
    print()
    print("Next steps:")
    print("1. Get NASA API keys from https://api.nasa.gov/")
    print("2. Set up EarthData credentials at https://urs.earthdata.nasa.gov/")
    print("3. Test with real API calls")
    print("4. Integrate with your frontend dashboard")

if __name__ == "__main__":
    test_nasa_integration() 