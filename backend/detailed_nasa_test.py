#!/usr/bin/env python3
"""
Detailed NASA API test - shows exactly what's happening with API calls
"""

import os
import sys
import json
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.nasa_services import nasa_services

def detailed_nasa_test():
    """Test NASA API integration with detailed output"""
    print("🚀 Detailed NASA Integration Test for PTC Platform")
    print("=" * 60)
    
    # Test coordinates (San Francisco area)
    test_lat = 37.7749
    test_lon = -122.4194
    
    print(f"📍 Testing location: {test_lat}, {test_lon}")
    print(f"🔑 NASA API Key loaded: {'✅ YES' if nasa_services.nasa_api_key else '❌ NO'}")
    if nasa_services.nasa_api_key:
        print(f"    Key: {nasa_services.nasa_api_key[:10]}...{nasa_services.nasa_api_key[-4:]}")
    print()
    
    # Test 1: Satellite Imagery (Real API call)
    print("1. 🛰️  Testing NASA Satellite Imagery API...")
    imagery_data = nasa_services.get_satellite_imagery(test_lat, test_lon)
    print(f"   Status: {imagery_data.get('status', 'unknown')}")
    if 'imagery_url' in imagery_data:
        print(f"   📸 Imagery URL: {imagery_data['imagery_url']}")
    if 'error' in imagery_data:
        print(f"   ❌ Error: {imagery_data['error']}")
    print(f"   📊 Full Response: {json.dumps(imagery_data, indent=2)}")
    print()
    
    # Test 2: Earth Assets (Real API call)
    print("2. 🌍 Testing NASA Earth Assets API...")
    assets_data = nasa_services.get_earth_assets(test_lat, test_lon)
    print(f"   Status: {assets_data.get('status', 'unknown')}")
    if 'assets_count' in assets_data:
        print(f"   📦 Assets found: {assets_data['assets_count']}")
    if 'error' in assets_data:
        print(f"   ❌ Error: {assets_data['error']}")
    print(f"   📊 Full Response: {json.dumps(assets_data, indent=2)}")
    print()
    
    # Test 3: CO2 Data (Enhanced with real validation)
    print("3. 🌡️  Testing CO2 concentration data...")
    co2_data = nasa_services.get_co2_concentrations(test_lat, test_lon)
    print(f"   CO2 Level: {co2_data.get('co2_concentration', 'N/A')} ppm")
    print(f"   Confidence: {co2_data.get('confidence', 'N/A')}")
    print(f"   Imagery Validated: {co2_data.get('imagery_validated', 'N/A')}")
    print(f"   Data Source: {co2_data.get('data_source', 'N/A')}")
    print()
    
    # Test 4: Temperature Data (Enhanced with real validation)
    print("4. 🌡️  Testing temperature data...")
    temp_data = nasa_services.get_temperature_data(test_lat, test_lon)
    print(f"   Temperature: {temp_data.get('temperature', 'N/A')}°C")
    print(f"   Anomaly: {temp_data.get('temperature_anomaly', 'N/A')}°C")
    print(f"   Confidence: {temp_data.get('confidence', 'N/A')}")
    print(f"   Imagery Validated: {temp_data.get('imagery_validated', 'N/A')}")
    print()
    
    # Test 5: Biomass Data (Enhanced with real validation)
    print("5. 🌿 Testing biomass data...")
    biomass_data = nasa_services.get_biomass_data(test_lat, test_lon)
    print(f"   Biomass Density: {biomass_data.get('biomass_density', 'N/A')} tons/ha")
    print(f"   Vegetation Type: {biomass_data.get('vegetation_type', 'N/A')}")
    print(f"   Confidence: {biomass_data.get('confidence', 'N/A')}")
    print(f"   Imagery Validated: {biomass_data.get('imagery_validated', 'N/A')}")
    print()
    
    # Test 6: Comprehensive Optimization
    print("6. 🎯 Testing comprehensive optimization...")
    optimization_data = nasa_services.get_intervention_optimization_data(test_lat, test_lon)
    recommendations = optimization_data.get('intervention_recommendations', {})
    print(f"   Optimal Intervention: {recommendations.get('optimal_intervention_type', 'N/A')}")
    print(f"   Priority: {recommendations.get('deployment_priority', 'N/A')}")
    print(f"   Expected Impact: {recommendations.get('expected_impact', 'N/A')}")
    print(f"   Confidence Score: {recommendations.get('confidence_score', 'N/A')}")
    print(f"   🔄 API Status: {optimization_data.get('api_status', 'N/A')}")
    print()
    
    # Summary
    print("🎉 Detailed NASA Integration Test Complete!")
    print("=" * 60)
    
    # Check if we're actually connected to NASA
    if imagery_data.get('status') == 'success':
        print("✅ SUCCESS: Your PTC platform is CONNECTED to NASA!")
        print("🛰️  Real satellite imagery URLs being generated")
        print("🌍 Location validation through NASA Earth observation")
        print("📊 Enhanced climate data based on actual satellite validation")
    elif imagery_data.get('status') == 'api_error':
        print("⚠️  API ERROR: NASA responded but with an error")
        print(f"   Error details: {imagery_data.get('error', 'Unknown')}")
        print("   This might be due to API limits, invalid coordinates, or service issues")
    else:
        print("❌ ISSUE: Not connecting to NASA APIs")
        print("   Check your API key and internet connection")
    
    print()
    print("🔍 Business Impact:")
    print("• Climate operators can see real environmental conditions")
    print("• Intervention recommendations based on actual NASA satellite data")
    print("• Government-grade data credibility for funding and partnerships")
    print("• Location validation for deployment decisions")

if __name__ == "__main__":
    detailed_nasa_test()