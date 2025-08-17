#!/usr/bin/env python3
"""
Comprehensive Accuracy Test - Measures the actual ML accuracy with hundreds of test cases
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ml_engine import ClimateMLEngine
import numpy as np
import time

def generate_comprehensive_test_cases():
    """Generate hundreds of realistic test cases for comprehensive accuracy testing."""
    test_cases = []
    
    # HIGH SUITABILITY CASES (should score 0.8-1.0)
    # Generate 50 high suitability cases with variations
    for i in range(50):
        test_cases.append({
            'latitude': np.random.uniform(-60, 60),
            'longitude': np.random.uniform(-180, 180),
            'intervention_type': np.random.choice(['biochar', 'DAC', 'afforestation', 'enhanced_weathering']),
            'temperature': np.random.uniform(15, 35),
            'co2_concentration': np.random.uniform(430, 460),  # High CO2
            'biomass_density': np.random.uniform(65, 100),     # High biomass
            'temperature_anomaly': np.random.uniform(1.3, 3.0), # High temp
            'humidity': np.random.uniform(60, 90),
            'pressure': np.random.uniform(1000, 1020),
            'wind_speed': np.random.uniform(5, 15),
            'precipitation': np.random.uniform(20, 60),
            'aerosol_optical_depth': np.random.uniform(0.1, 0.4),
            'solar_irradiance': np.random.uniform(850, 1100),
            'albedo': np.random.uniform(0.2, 0.35),
            'carbon_storage_potential': np.random.uniform(70, 100),
            'temperature_trend': np.random.uniform(0.2, 0.6),
            'co2_trend': np.random.uniform(2.5, 4.5),
            'precipitation_trend': np.random.uniform(0.03, 0.08),
            'climate_zone': np.random.choice(['tropical', 'temperate', 'boreal']),
            'vegetation_type': np.random.choice(['tropical_forest', 'temperate_forest', 'boreal_forest']),
            'expected': 'high',
            'expected_score': np.random.uniform(0.8, 1.0)
        })
    
    # MEDIUM SUITABILITY CASES (should score 0.5-0.7)
    # Generate 50 medium suitability cases with variations
    for i in range(50):
        test_cases.append({
            'latitude': np.random.uniform(-60, 60),
            'longitude': np.random.uniform(-180, 180),
            'intervention_type': np.random.choice(['biochar', 'DAC', 'afforestation', 'enhanced_weathering']),
            'temperature': np.random.uniform(10, 25),
            'co2_concentration': np.random.uniform(410, 425),  # Medium CO2
            'biomass_density': np.random.uniform(35, 60),      # Medium biomass
            'temperature_anomaly': np.random.uniform(0.8, 1.4), # Medium temp
            'humidity': np.random.uniform(45, 70),
            'pressure': np.random.uniform(1005, 1015),
            'wind_speed': np.random.uniform(10, 20),
            'precipitation': np.random.uniform(15, 35),
            'aerosol_optical_depth': np.random.uniform(0.2, 0.45),
            'solar_irradiance': np.random.uniform(900, 1050),
            'albedo': np.random.uniform(0.25, 0.4),
            'carbon_storage_potential': np.random.uniform(40, 65),
            'temperature_trend': np.random.uniform(0.1, 0.4),
            'co2_trend': np.random.uniform(1.5, 3.0),
            'precipitation_trend': np.random.uniform(0.01, 0.06),
            'climate_zone': np.random.choice(['temperate', 'mediterranean', 'boreal']),
            'vegetation_type': np.random.choice(['grassland', 'temperate_forest', 'boreal_forest']),
            'expected': 'medium',
            'expected_score': np.random.uniform(0.5, 0.7)
        })
    
    # LOW SUITABILITY CASES (should score 0.1-0.4)
    # Generate 50 low suitability cases with variations
    for i in range(50):
        test_cases.append({
            'latitude': np.random.uniform(-60, 60),
            'longitude': np.random.uniform(-180, 180),
            'intervention_type': np.random.choice(['biochar', 'DAC', 'afforestation', 'enhanced_weathering']),
            'temperature': np.random.uniform(-15, 40),
            'co2_concentration': np.random.uniform(380, 415),  # Low-medium CO2
            'biomass_density': np.random.uniform(5, 35),       # Low biomass
            'temperature_anomaly': np.random.uniform(0.1, 2.5), # Variable temp
            'humidity': np.random.uniform(15, 60),
            'pressure': np.random.uniform(990, 1010),
            'wind_speed': np.random.uniform(15, 35),
            'precipitation': np.random.uniform(0, 25),
            'aerosol_optical_depth': np.random.uniform(0.3, 0.7),
            'solar_irradiance': np.random.uniform(700, 1200),
            'albedo': np.random.uniform(0.3, 0.7),
            'carbon_storage_potential': np.random.uniform(10, 45),
            'temperature_trend': np.random.uniform(-0.3, 0.7),
            'co2_trend': np.random.uniform(0.5, 2.5),
            'precipitation_trend': np.random.uniform(-0.02, 0.04),
            'climate_zone': np.random.choice(['desert', 'arctic', 'mediterranean']),
            'vegetation_type': np.random.choice(['desert', 'tundra', 'grassland']),
            'expected': 'low',
            'expected_score': np.random.uniform(0.1, 0.4)
        })
    
    # EDGE CASES - Borderline scenarios that test model robustness
    # Generate 25 edge cases
    edge_scenarios = [
        # Borderline high-medium
        {'co2': 428, 'biomass': 64, 'temp': 1.2, 'expected': 'medium'},
        {'co2': 429, 'biomass': 66, 'temp': 1.3, 'expected': 'high'},
        {'co2': 427, 'biomass': 63, 'temp': 1.1, 'expected': 'medium'},
        
        # Borderline medium-low
        {'co2': 412, 'biomass': 29, 'temp': 0.7, 'expected': 'low'},
        {'co2': 413, 'biomass': 31, 'temp': 0.8, 'expected': 'medium'},
        {'co2': 411, 'biomass': 28, 'temp': 0.6, 'expected': 'low'},
        
        # Mixed indicators
        {'co2': 435, 'biomass': 30, 'temp': 2.0, 'expected': 'medium'},  # High CO2, low biomass
        {'co2': 405, 'biomass': 80, 'temp': 0.3, 'expected': 'medium'},  # Low CO2, high biomass
        {'co2': 420, 'biomass': 45, 'temp': 2.5, 'expected': 'medium'},  # Medium CO2, medium biomass, high temp
        
        # Extreme cases
        {'co2': 500, 'biomass': 120, 'temp': 4.0, 'expected': 'high'},   # Extreme high
        {'co2': 350, 'biomass': 2, 'temp': 0.01, 'expected': 'low'},      # Extreme low
        {'co2': 415, 'biomass': 50, 'temp': 1.0, 'expected': 'medium'},  # Perfect medium
    ]
    
    for scenario in edge_scenarios:
        for i in range(2):  # 2 variations per edge scenario
            test_cases.append({
                'latitude': np.random.uniform(-60, 60),
                'longitude': np.random.uniform(-180, 180),
                'intervention_type': np.random.choice(['biochar', 'DAC', 'afforestation', 'enhanced_weathering']),
                'temperature': np.random.uniform(-20, 40),
                'co2_concentration': scenario['co2'] + np.random.normal(0, 1),
                'biomass_density': max(0, scenario['biomass'] + np.random.normal(0, 2)),
                'temperature_anomaly': max(0, scenario['temp'] + np.random.normal(0, 0.1)),
                'humidity': np.random.uniform(20, 90),
                'pressure': np.random.uniform(950, 1050),
                'wind_speed': np.random.uniform(0, 30),
                'precipitation': np.random.uniform(0, 50),
                'aerosol_optical_depth': np.random.uniform(0.05, 0.6),
                'solar_irradiance': np.random.uniform(700, 1200),
                'albedo': np.random.uniform(0.1, 0.7),
                'carbon_storage_potential': np.random.uniform(0, 100),
                'temperature_trend': np.random.uniform(-0.5, 0.7),
                'co2_trend': np.random.uniform(0, 5),
                'precipitation_trend': np.random.uniform(-0.1, 0.1),
                'climate_zone': np.random.choice(['tropical', 'temperate', 'boreal', 'arctic', 'desert', 'mediterranean']),
                'vegetation_type': np.random.choice(['temperate_forest', 'tropical_forest', 'boreal_forest', 'grassland', 'tundra', 'desert']),
                'expected': scenario['expected'],
                'expected_score': np.random.uniform(0.3, 0.9)
            })
    
    return test_cases

def test_comprehensive_accuracy():
    """Test the ML accuracy with hundreds of realistic test cases."""
    print("🎯 Testing Comprehensive ML Accuracy")
    print("=" * 60)
    
    # Initialize the ML engine
    print("📊 Initializing ML engine...")
    ml_engine = ClimateMLEngine()
    
    # Generate comprehensive test cases
    print("\n🧪 Generating comprehensive test cases...")
    test_cases = generate_comprehensive_test_cases()
    
    print(f"📋 Generated {len(test_cases)} test cases:")
    print(f"   - High suitability: {len([c for c in test_cases if c['expected'] == 'high'])}")
    print(f"   - Medium suitability: {len([c for c in test_cases if c['expected'] == 'medium'])}")
    print(f"   - Low suitability: {len([c for c in test_cases if c['expected'] == 'low'])}")
    
    # Test each case
    print(f"\n🧪 Testing {len(test_cases)} comprehensive test cases...")
    print("-" * 60)
    
    correct_predictions = 0
    total_predictions = len(test_cases)
    prediction_times = []
    
    # Track accuracy by category
    category_results = {'high': {'correct': 0, 'total': 0}, 
                       'medium': {'correct': 0, 'total': 0}, 
                       'low': {'correct': 0, 'total': 0}}
    
    for i, test_case in enumerate(test_cases, 1):
        if i % 50 == 0:  # Progress update every 50 tests
            print(f"   Progress: {i}/{total_predictions} tests completed...")
        
        # Get prediction
        start_time = time.time()
        result = ml_engine.assess_site_suitability(test_case)
        prediction_time = time.time() - start_time
        prediction_times.append(prediction_time)
        
        if result.get('success'):
            # Check if prediction matches expected
            if result['suitability_class'] == test_case['expected']:
                correct_predictions += 1
                category_results[test_case['expected']]['correct'] += 1
            category_results[test_case['expected']]['total'] += 1
        else:
            print(f"   ❌ Test case {i} failed: {result.get('error', 'Unknown error')}")
    
    # Calculate overall accuracy
    accuracy = correct_predictions / total_predictions
    avg_prediction_time = np.mean(prediction_times)
    
    # Calculate category-specific accuracy
    category_accuracy = {}
    for category, counts in category_results.items():
        if counts['total'] > 0:
            category_accuracy[category] = counts['correct'] / counts['total']
        else:
            category_accuracy[category] = 0.0
    
    print(f"\n📈 COMPREHENSIVE ACCURACY RESULTS")
    print("=" * 60)
    print(f"Total Test Cases: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}/{total_predictions}")
    print(f"Overall Accuracy: {accuracy:.1%}")
    print(f"Average Prediction Time: {avg_prediction_time:.4f}s")
    
    print(f"\n📊 ACCURACY BY CATEGORY:")
    print(f"   High Suitability: {category_accuracy['high']:.1%} ({category_results['high']['correct']}/{category_results['high']['total']})")
    print(f"   Medium Suitability: {category_accuracy['medium']:.1%} ({category_results['medium']['correct']}/{category_results['medium']['total']})")
    print(f"   Low Suitability: {category_accuracy['low']:.1%} ({category_results['low']['correct']}/{category_results['low']['total']})")
    
    # Final assessment
    print(f"\n🎯 COMPREHENSIVE ACCURACY ASSESSMENT")
    print("=" * 60)
    
    if accuracy >= 0.95:
        print(f"🎉 EXCELLENT! {accuracy:.1%} accuracy - You can claim 95%+!")
    elif accuracy >= 0.90:
        print(f"🎉 OUTSTANDING! {accuracy:.1%} accuracy - You can claim 90%+!")
    elif accuracy >= 0.85:
        print(f"✅ VERY GOOD! {accuracy:.1%} accuracy - You can claim 85%+!")
    elif accuracy >= 0.80:
        print(f"✅ GOOD! {accuracy:.1%} accuracy - You can claim 80%+!")
    elif accuracy >= 0.75:
        print(f"⚠️  FAIR! {accuracy:.1%} accuracy - Needs improvement")
    else:
        print(f"❌ NEEDS WORK: {accuracy:.1%} accuracy - Significant improvement needed")
    
    return accuracy, avg_prediction_time, category_accuracy

if __name__ == "__main__":
    print("🎯 Starting Comprehensive Accuracy Test")
    print("=" * 60)
    
    try:
        accuracy, avg_time, category_accuracy = test_comprehensive_accuracy()
        
        print(f"\n🎯 Final Result: {accuracy:.1%} accuracy achieved!")
        print(f"⚡ Average prediction time: {avg_time:.4f}s")
        
        if accuracy >= 0.90:
            print("🚀 SUCCESS! Your platform has excellent accuracy!")
        elif accuracy >= 0.80:
            print("✅ GOOD! Your platform has good accuracy!")
        else:
            print("🔧 Your platform needs accuracy improvements.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
