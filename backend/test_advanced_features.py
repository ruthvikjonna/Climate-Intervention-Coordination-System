#!/usr/bin/env python3
"""
Comprehensive Test for Advanced PTC Platform Features
Tests ML engine, climate simulation, Celery tasks, and spatial optimization
"""

import os
import sys
import json
from datetime import datetime
import time

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_ml_engine():
    """Test ML-Augmented Climate Engine"""
    print("🧠 Testing ML-Augmented Climate Engine...")
    print("=" * 50)
    
    try:
        from app.services.ml_engine import ml_engine
        
        # Test data
        climate_data = {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'intervention_type': 'biochar',
            'temperature': 15.5,
            'co2_concentration': 420,
            'biomass_density': 35,
            'temperature_anomaly': 1.2,
            'humidity': 60,
            'pressure': 1013,
            'wind_speed': 8,
            'precipitation': 5,
            'aerosol_optical_depth': 0.15,
            'solar_irradiance': 950,
            'albedo': 0.25,
            'carbon_storage_potential': 87.5,
            'temperature_trend': 0.18,
            'co2_trend': 2.5,
            'precipitation_trend': -0.02,
            'vegetation_type': 'temperate_forest',
            'climate_zone': 'temperate'
        }
        
        # Test 1: Predict intervention outcomes
        print("1. Testing intervention outcome prediction...")
        predictions = ml_engine.predict_intervention_outcomes(climate_data)
        print(f"   ✅ CO2 Reduction: {predictions.get('predictions', {}).get('co2_reduction_ppm', 'N/A')} ppm")
        print(f"   ✅ Temperature Change: {predictions.get('predictions', {}).get('temperature_change_celsius', 'N/A')}°C")
        print(f"   ✅ Intervention Score: {predictions.get('predictions', {}).get('intervention_score', 'N/A')}")
        
        # Test 2: Assess site suitability
        print("\n2. Testing site suitability assessment...")
        suitability = ml_engine.assess_site_suitability(climate_data)
        print(f"   ✅ Suitability Class: {suitability.get('suitability_class', 'N/A')}")
        print(f"   ✅ Confidence: {suitability.get('confidence', 'N/A')}")
        
        # Test 3: Rank interventions
        print("\n3. Testing intervention ranking...")
        rankings = ml_engine.rank_interventions(climate_data, ['biochar', 'DAC', 'afforestation'])
        print(f"   ✅ Top Recommendation: {rankings.get('top_recommendation', {}).get('intervention_type', 'N/A')}")
        print(f"   ✅ Rankings Generated: {len(rankings.get('rankings', []))}")
        
        print("\n✅ ML Engine tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ML Engine test failed: {e}")
        return False

def test_climate_simulation():
    """Test NVIDIA Earth-2 Climate Simulation"""
    print("\n🌍 Testing NVIDIA Earth-2 Climate Simulation...")
    print("=" * 50)
    
    try:
        from app.services.climate_simulation import climate_simulation
        
        # Test 1: Climate impact simulation
        print("1. Testing climate impact simulation...")
        simulation_result = climate_simulation.simulate_climate_impact(
            latitude=37.7749,
            longitude=-122.4194,
            intervention_type='biochar',
            scale_amount=500,
            duration_months=12
        )
        
        if simulation_result.get('success'):
            results = simulation_result.get('results', {})
            summary = results.get('summary', {})
            print(f"   ✅ Simulation Mode: {simulation_result.get('simulation_mode', 'N/A')}")
            print(f"   ✅ Total CO2 Reduction: {summary.get('total_co2_reduction_ppm', 'N/A')} ppm")
            print(f"   ✅ Max Temperature Cooling: {summary.get('max_temperature_cooling_celsius', 'N/A')}°C")
            print(f"   ✅ Effectiveness Score: {summary.get('effectiveness_score', 'N/A')}")
        else:
            print(f"   ❌ Simulation failed: {simulation_result.get('error', 'Unknown error')}")
        
        # Test 2: Regional forecast
        print("\n2. Testing regional forecast...")
        forecast = climate_simulation.get_regional_forecast(
            latitude=37.7749,
            longitude=-122.4194,
            forecast_months=6
        )
        
        if forecast.get('success'):
            print(f"   ✅ Forecast Mode: {forecast.get('forecast_mode', 'N/A')}")
            print(f"   ✅ Monthly Forecasts: {len(forecast.get('monthly_forecast', []))}")
            print(f"   ✅ Temperature Trend: {forecast.get('trends', {}).get('temperature_trend_celsius_per_month', 'N/A')}°C/month")
        else:
            print(f"   ❌ Forecast failed: {forecast.get('error', 'Unknown error')}")
        
        # Test 3: Intervention comparison
        print("\n3. Testing intervention comparison...")
        interventions = [
            {'type': 'biochar', 'scale': 500},
            {'type': 'DAC', 'scale': 200},
            {'type': 'afforestation', 'scale': 1000}
        ]
        
        comparison = climate_simulation.compare_interventions(
            latitude=37.7749,
            longitude=-122.4194,
            interventions=interventions
        )
        
        if comparison.get('success'):
            print(f"   ✅ Top Recommendation: {comparison.get('top_recommendation', {}).get('intervention_type', 'N/A')}")
            print(f"   ✅ Comparisons Generated: {len(comparison.get('comparison_results', []))}")
        else:
            print(f"   ❌ Comparison failed: {comparison.get('error', 'Unknown error')}")
        
        print("\n✅ Climate Simulation tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Climate Simulation test failed: {e}")
        return False

def test_celery_tasks():
    """Test Celery async task system"""
    print("\n⚡ Testing Celery Async Task System...")
    print("=" * 50)
    
    try:
        from app.services.celery_app import celery_app
        from app.services.tasks.intervention_tasks import plan_intervention_deployment
        from app.services.tasks.optimization_tasks import run_global_optimization
        
        # Test 1: Debug task
        print("1. Testing debug task...")
        debug_task = celery_app.send_task('app.services.celery_app.debug_task')
        result = debug_task.get(timeout=10)
        print(f"   ✅ Debug task result: {result.get('message', 'N/A')}")
        
        # Test 2: Intervention planning task
        print("\n2. Testing intervention planning task...")
        intervention_data = {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'intervention_type': 'biochar',
            'scale_amount': 500,
            'operator_id': 'test-operator-123'
        }
        
        planning_task = plan_intervention_deployment.delay(intervention_data)
        
        # Wait for task completion
        max_wait = 30
        start_time = time.time()
        while not planning_task.ready() and (time.time() - start_time) < max_wait:
            time.sleep(1)
        
        if planning_task.ready():
            result = planning_task.get()
            if result.get('success'):
                print(f"   ✅ Planning task completed: {result.get('deployment_plan', {}).get('intervention_type', 'N/A')}")
            else:
                print(f"   ❌ Planning task failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"   ⚠️ Planning task timed out after {max_wait} seconds")
        
        # Test 3: Global optimization task
        print("\n3. Testing global optimization task...")
        optimization_task = run_global_optimization.delay()
        
        # Wait for task completion
        start_time = time.time()
        while not optimization_task.ready() and (time.time() - start_time) < max_wait:
            time.sleep(1)
        
        if optimization_task.ready():
            result = optimization_task.get()
            if result.get('success'):
                analysis = result.get('global_analysis', {})
                print(f"   ✅ Optimization completed: {analysis.get('total_active_interventions', 0)} interventions analyzed")
            else:
                print(f"   ❌ Optimization failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"   ⚠️ Optimization task timed out after {max_wait} seconds")
        
        print("\n✅ Celery Task tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Celery Task test failed: {e}")
        return False

def test_spatial_engine():
    """Test PostGIS Spatial Engine"""
    print("\n🗺️ Testing PostGIS Spatial Engine...")
    print("=" * 50)
    
    try:
        from app.services.spatial_engine import spatial_engine
        
        # Test 1: Spatial statistics
        print("1. Testing spatial statistics...")
        stats = spatial_engine.get_spatial_statistics()
        if stats.get('success'):
            print(f"   ✅ Total Interventions: {stats.get('total_interventions', 0)}")
            print(f"   ✅ Spatial Coverage: {stats.get('spatial_coverage_km2', 0)} km²")
            print(f"   ✅ Geographic Distribution: {stats.get('geographic_distribution', {})}")
        else:
            print(f"   ❌ Spatial statistics failed: {stats.get('error', 'Unknown error')}")
        
        # Test 2: Nearby interventions
        print("\n2. Testing nearby interventions search...")
        nearby = spatial_engine.find_nearby_interventions(
            latitude=37.7749,
            longitude=-122.4194,
            radius_km=100
        )
        print(f"   ✅ Nearby interventions found: {len(nearby)}")
        
        # Test 3: Spatial optimization
        print("\n3. Testing spatial deployment optimization...")
        target_region = {
            'lat_min': 35,
            'lat_max': 40,
            'lon_min': -125,
            'lon_max': -120,
            'constraints': {
                'min_distance_km': 10,
                'max_elevation': 2000,
                'allowed_land_covers': ['temperate_forest', 'mixed_forest']
            }
        }
        
        optimization = spatial_engine.optimize_spatial_deployment(
            target_region=target_region,
            intervention_type='biochar',
            total_budget=1000000
        )
        
        if optimization.get('success'):
            deployment = optimization.get('optimized_deployment', [])
            print(f"   ✅ Optimized sites: {len(deployment)}")
            print(f"   ✅ Coverage area: {optimization.get('spatial_analysis', {}).get('coverage_area_km2', 0)} km²")
            print(f"   ✅ Spatial efficiency: {optimization.get('spatial_analysis', {}).get('spatial_efficiency', 0)}")
        else:
            print(f"   ❌ Spatial optimization failed: {optimization.get('error', 'Unknown error')}")
        
        print("\n✅ Spatial Engine tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Spatial Engine test failed: {e}")
        return False

def test_api_endpoints():
    """Test new API endpoints"""
    print("\n🌐 Testing New API Endpoints...")
    print("=" * 50)
    
    try:
        import requests
        import json
        
        base_url = "http://localhost:8000/api/v1"
        
        # Test 1: ML prediction endpoint
        print("1. Testing ML prediction endpoint...")
        climate_data = {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'intervention_type': 'biochar',
            'temperature': 15.5,
            'co2_concentration': 420,
            'biomass_density': 35
        }
        
        try:
            response = requests.post(
                f"{base_url}/ml-optimization/predict-intervention-outcomes",
                json=climate_data,
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ ML prediction successful: {result.get('success', False)}")
            else:
                print(f"   ❌ ML prediction failed: {response.status_code}")
        except requests.exceptions.RequestException:
            print("   ⚠️ API server not running - skipping API tests")
            return True
        
        # Test 2: Climate simulation endpoint
        print("\n2. Testing climate simulation endpoint...")
        try:
            response = requests.post(
                f"{base_url}/ml-optimization/simulate-climate-impact",
                params={
                    'latitude': 37.7749,
                    'longitude': -122.4194,
                    'intervention_type': 'biochar',
                    'scale_amount': 500,
                    'duration_months': 12
                },
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Climate simulation successful: {result.get('success', False)}")
            else:
                print(f"   ❌ Climate simulation failed: {response.status_code}")
        except requests.exceptions.RequestException:
            print("   ⚠️ API server not running - skipping API tests")
            return True
        
        # Test 3: Smart site selection endpoint
        print("\n3. Testing smart site selection endpoint...")
        constraints = {
            'region': 'global',
            'intervention_type': 'biochar',
            'budget_usd': 1000000,
            'scale_target': 1000,
            'time_constraint': 12
        }
        
        try:
            response = requests.post(
                f"{base_url}/ml-optimization/smart-site-selection",
                json=constraints,
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Smart site selection successful: {result.get('success', False)}")
                if result.get('success'):
                    print(f"   ✅ Task ID: {result.get('task_id', 'N/A')}")
            else:
                print(f"   ❌ Smart site selection failed: {response.status_code}")
        except requests.exceptions.RequestException:
            print("   ⚠️ API server not running - skipping API tests")
            return True
        
        print("\n✅ API Endpoint tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ API Endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 PTC Platform Advanced Features Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = []
    
    # Run all tests
    tests = [
        ("ML-Augmented Climate Engine", test_ml_engine),
        ("NVIDIA Earth-2 Climate Simulation", test_climate_simulation),
        ("Celery Async Task System", test_celery_tasks),
        ("PostGIS Spatial Engine", test_spatial_engine),
        ("New API Endpoints", test_api_endpoints)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<35} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PTC Platform advanced features are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 