"""
ML-Augmented Climate Engine for PTC Platform
Implements the ML models mentioned in the README:
- Lasso/Ridge Regression for intervention outcome prediction
- Random Forest Classifier for site suitability assessment
- Boosting Models for intervention ranking
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import joblib
import os
from pathlib import Path

# ML Libraries
from sklearn.linear_model import Lasso, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import xgboost as xgb
import lightgbm as lgb

# Spatial libraries
from shapely.geometry import Point
import geopandas as gpd

class ClimateMLEngine:
    """
    ML-Augmented Climate Engine for intervention optimization
    """
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        # Initialize models
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        
        # Load or initialize models
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize or load trained models"""
        
        # 1. Lasso/Ridge Regression for CO₂ ppm and °C change prediction
        self.models['co2_regression'] = {
            'lasso': Lasso(alpha=0.1, random_state=42),
            'ridge': Ridge(alpha=1.0, random_state=42)
        }
        
        # 2. Random Forest Classifier for site suitability
        self.models['site_suitability'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        # 3. Boosting Models for intervention ranking
        self.models['intervention_ranking'] = {
            'xgboost': xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            ),
            'lightgbm': lgb.LGBMRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        }
        
        # Scalers for feature normalization
        self.scalers['features'] = StandardScaler()
        self.scalers['targets'] = StandardScaler()
        
        # Label encoders for categorical variables
        self.label_encoders['intervention_type'] = LabelEncoder()
        self.label_encoders['vegetation_type'] = LabelEncoder()
        self.label_encoders['climate_zone'] = LabelEncoder()
        
        # Try to load pre-trained models
        self._load_models()
        
    def _load_models(self):
        """Load pre-trained models if they exist"""
        try:
            for model_name, model in self.models.items():
                if isinstance(model, dict):
                    for submodel_name, submodel in model.items():
                        model_path = self.model_dir / f"{model_name}_{submodel_name}.joblib"
                        if model_path.exists():
                            self.models[model_name][submodel_name] = joblib.load(model_path)
                else:
                    model_path = self.model_dir / f"{model_name}.joblib"
                    if model_path.exists():
                        self.models[model_name] = joblib.load(model_path)
                        
            # Load scalers and encoders
            for name in ['features', 'targets']:
                scaler_path = self.model_dir / f"scaler_{name}.joblib"
                if scaler_path.exists():
                    self.scalers[name] = joblib.load(scaler_path)
                    
            for name in ['intervention_type', 'vegetation_type', 'climate_zone']:
                encoder_path = self.model_dir / f"encoder_{name}.joblib"
                if encoder_path.exists():
                    self.label_encoders[name] = joblib.load(encoder_path)
                    
            print("✅ Loaded pre-trained ML models")
            
        except Exception as e:
            print(f"⚠️ Could not load pre-trained models: {e}")
            print("Will train new models with available data")
    
    def _save_models(self):
        """Save trained models"""
        try:
            for model_name, model in self.models.items():
                if isinstance(model, dict):
                    for submodel_name, submodel in model.items():
                        model_path = self.model_dir / f"{model_name}_{submodel_name}.joblib"
                        joblib.dump(submodel, model_path)
                else:
                    model_path = self.model_dir / f"{model_name}.joblib"
                    joblib.dump(model, model_path)
            
            # Save scalers and encoders
            for name, scaler in self.scalers.items():
                scaler_path = self.model_dir / f"scaler_{name}.joblib"
                joblib.dump(scaler, scaler_path)
                
            for name, encoder in self.label_encoders.items():
                encoder_path = self.model_dir / f"encoder_{name}.joblib"
                joblib.dump(encoder, encoder_path)
                
            print("✅ Saved trained ML models")
            
        except Exception as e:
            print(f"❌ Error saving models: {e}")
    
    def prepare_features(self, climate_data: Dict[str, Any]) -> np.ndarray:
        """
        Prepare features for ML models from climate data
        """
        features = []
        
        # Geographic features
        features.extend([
            climate_data.get('latitude', 0),
            climate_data.get('longitude', 0),
            abs(climate_data.get('latitude', 0)),  # Distance from equator
        ])
        
        # Climate features
        features.extend([
            climate_data.get('temperature', 15),
            climate_data.get('temperature_anomaly', 0),
            climate_data.get('co2_concentration', 415),
            climate_data.get('humidity', 50),
            climate_data.get('pressure', 1013),
            climate_data.get('wind_speed', 5),
            climate_data.get('precipitation', 0),
            climate_data.get('aerosol_optical_depth', 0.1),
            climate_data.get('solar_irradiance', 1000),
            climate_data.get('albedo', 0.3),
        ])
        
        # Biomass and vegetation features
        features.extend([
            climate_data.get('biomass_density', 0),
            climate_data.get('carbon_storage_potential', 0),
        ])
        
        # Historical trends
        features.extend([
            climate_data.get('temperature_trend', 0),
            climate_data.get('co2_trend', 0),
            climate_data.get('precipitation_trend', 0),
        ])
        
        # Seasonal features
        current_date = datetime.now()
        features.extend([
            current_date.month,
            current_date.day,
            np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365),  # Seasonal cycle
            np.cos(2 * np.pi * current_date.timetuple().tm_yday / 365),
        ])
        
        # Encode categorical variables
        intervention_type = climate_data.get('intervention_type', 'unknown')
        vegetation_type = climate_data.get('vegetation_type', 'unknown')
        climate_zone = climate_data.get('climate_zone', 'temperate')
        
        # Fit encoders if needed and transform
        for name, value in [('intervention_type', intervention_type), 
                           ('vegetation_type', vegetation_type),
                           ('climate_zone', climate_zone)]:
            if not hasattr(self.label_encoders[name], 'classes_'):
                # Fit encoder with sample data
                sample_data = ['unknown', 'biochar', 'DAC', 'afforestation', 'monitoring']
                self.label_encoders[name].fit(sample_data)
            
            encoded_value = self.label_encoders[name].transform([value])[0]
            features.append(encoded_value)
        
        return np.array(features).reshape(1, -1)
    
    def predict_intervention_outcomes(self, climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict intervention outcomes using Lasso/Ridge Regression
        Returns: projected °C cooling, CO₂ ppm reduction, intervention score
        """
        try:
            features = self.prepare_features(climate_data)
            
            # Scale features
            if not hasattr(self.scalers['features'], 'mean_'):
                # Fit scaler with sample data
                sample_features = np.random.randn(100, features.shape[1])
                self.scalers['features'].fit(sample_features)
            
            features_scaled = self.scalers['features'].transform(features)
            
            predictions = {}
            
            # Predict CO₂ reduction
            if hasattr(self.models['co2_regression']['lasso'], 'coef_'):
                co2_lasso = self.models['co2_regression']['lasso'].predict(features_scaled)[0]
                co2_ridge = self.models['co2_regression']['ridge'].predict(features_scaled)[0]
                predictions['co2_reduction_ppm'] = (co2_lasso + co2_ridge) / 2
            else:
                # Use rule-based prediction if model not trained
                base_co2 = climate_data.get('co2_concentration', 415)
                predictions['co2_reduction_ppm'] = max(0, (base_co2 - 400) * 0.1)
            
            # Predict temperature change
            temp_anomaly = climate_data.get('temperature_anomaly', 0)
            predictions['temperature_change_celsius'] = -temp_anomaly * 0.3  # Cooling effect
            
            # Calculate intervention score
            co2_score = min(1.0, predictions['co2_reduction_ppm'] / 10)
            temp_score = min(1.0, abs(predictions['temperature_change_celsius']) / 2)
            biomass_score = min(1.0, climate_data.get('biomass_density', 0) / 50)
            
            predictions['intervention_score'] = (co2_score + temp_score + biomass_score) / 3
            
            return {
                'success': True,
                'predictions': predictions,
                'model_confidence': 0.85 if hasattr(self.models['co2_regression']['lasso'], 'coef_') else 0.6,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'predictions': {
                    'co2_reduction_ppm': 0,
                    'temperature_change_celsius': 0,
                    'intervention_score': 0
                }
            }
    
    def assess_site_suitability(self, climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess site suitability using Random Forest Classifier
        Returns: High/Medium/Low effectiveness tiers
        """
        try:
            features = self.prepare_features(climate_data)
            
            if hasattr(self.models['site_suitability'], 'classes_'):
                # Use trained model
                suitability_class = self.models['site_suitability'].predict(features)[0]
                confidence = max(self.models['site_suitability'].predict_proba(features)[0])
            else:
                # Rule-based assessment
                co2_level = climate_data.get('co2_concentration', 415)
                biomass = climate_data.get('biomass_density', 0)
                temp_anomaly = climate_data.get('temperature_anomaly', 0)
                
                # Calculate suitability score
                score = 0
                if co2_level > 420: score += 2
                if biomass > 30: score += 2
                if temp_anomaly > 1.0: score += 1
                
                if score >= 4:
                    suitability_class = 'high'
                    confidence = 0.9
                elif score >= 2:
                    suitability_class = 'medium'
                    confidence = 0.7
                else:
                    suitability_class = 'low'
                    confidence = 0.6
            
            return {
                'success': True,
                'suitability_class': suitability_class,
                'confidence': confidence,
                'assessment_factors': {
                    'co2_level': climate_data.get('co2_concentration', 415),
                    'biomass_density': climate_data.get('biomass_density', 0),
                    'temperature_anomaly': climate_data.get('temperature_anomaly', 0),
                    'vegetation_type': climate_data.get('vegetation_type', 'unknown')
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'suitability_class': 'low',
                'confidence': 0.5
            }
    
    def rank_interventions(self, climate_data: Dict[str, Any], 
                          intervention_types: List[str] = None) -> Dict[str, Any]:
        """
        Rank interventions by predicted impact using Boosting Models
        """
        if intervention_types is None:
            intervention_types = ['biochar', 'DAC', 'afforestation', 'enhanced_weathering']
        
        try:
            rankings = []
            
            for intervention_type in intervention_types:
                # Create data for this intervention type
                intervention_data = climate_data.copy()
                intervention_data['intervention_type'] = intervention_type
                
                features = self.prepare_features(intervention_data)
                
                # Get predictions from boosting models
                impact_score = 0
                model_count = 0
                
                for model_name, model in self.models['intervention_ranking'].items():
                    if hasattr(model, 'feature_importances_'):
                        # Use trained model
                        score = model.predict(features)[0]
                        impact_score += score
                        model_count += 1
                
                if model_count == 0:
                    # Rule-based scoring
                    base_score = 0
                    if intervention_type == 'biochar' and climate_data.get('biomass_density', 0) > 30:
                        base_score = 0.8
                    elif intervention_type == 'DAC' and climate_data.get('co2_concentration', 415) > 420:
                        base_score = 0.9
                    elif intervention_type == 'afforestation' and climate_data.get('biomass_density', 0) > 20:
                        base_score = 0.7
                    else:
                        base_score = 0.5
                    
                    impact_score = base_score
                else:
                    impact_score /= model_count
                
                # Calculate cost-efficiency (simplified)
                cost_efficiency = impact_score / max(0.1, climate_data.get('cost_per_tonne', 100) / 100)
                
                rankings.append({
                    'intervention_type': intervention_type,
                    'impact_score': impact_score,
                    'cost_efficiency': cost_efficiency,
                    'recommended_scale': self._calculate_recommended_scale(intervention_type, climate_data),
                    'deployment_priority': self._get_priority(impact_score)
                })
            
            # Sort by impact score
            rankings.sort(key=lambda x: x['impact_score'], reverse=True)
            
            return {
                'success': True,
                'rankings': rankings,
                'top_recommendation': rankings[0] if rankings else None,
                'model_confidence': 0.8 if model_count > 0 else 0.6,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'rankings': []
            }
    
    def _calculate_recommended_scale(self, intervention_type: str, climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate recommended scale for intervention"""
        base_scale = 100  # tonnes CO2 equivalent
        
        if intervention_type == 'biochar':
            biomass_factor = climate_data.get('biomass_density', 0) / 50
            scale = base_scale * biomass_factor
        elif intervention_type == 'DAC':
            co2_factor = climate_data.get('co2_concentration', 415) / 400
            scale = base_scale * co2_factor
        elif intervention_type == 'afforestation':
            biomass_factor = climate_data.get('biomass_density', 0) / 30
            scale = base_scale * biomass_factor
        else:
            scale = base_scale
        
        return {
            'amount': max(10, min(1000, scale)),
            'unit': 'tonnes_co2' if intervention_type in ['biochar', 'DAC'] else 'hectares',
            'estimated_cost': scale * climate_data.get('cost_per_tonne', 100)
        }
    
    def _get_priority(self, impact_score: float) -> str:
        """Get deployment priority based on impact score"""
        if impact_score > 0.8:
            return 'high'
        elif impact_score > 0.6:
            return 'medium'
        else:
            return 'low'
    
    def train_models(self, training_data: List[Dict[str, Any]]):
        """
        Train ML models with historical data
        """
        if not training_data:
            print("⚠️ No training data provided")
            return
        
        try:
            # Prepare training data
            X = []
            y_co2 = []
            y_temp = []
            y_suitability = []
            y_ranking = []
            
            for data_point in training_data:
                features = self.prepare_features(data_point).flatten()
                X.append(features)
                
                # Targets for different models
                y_co2.append(data_point.get('co2_reduction_actual', 0))
                y_temp.append(data_point.get('temperature_change_actual', 0))
                y_suitability.append(data_point.get('suitability_actual', 'low'))
                y_ranking.append(data_point.get('impact_score_actual', 0.5))
            
            X = np.array(X)
            
            # Split data
            X_train, X_test, y_co2_train, y_co2_test = train_test_split(
                X, y_co2, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scalers['features'].fit_transform(X_train)
            X_test_scaled = self.scalers['features'].transform(X_test)
            
            # Train CO2 regression models
            self.models['co2_regression']['lasso'].fit(X_train_scaled, y_co2_train)
            self.models['co2_regression']['ridge'].fit(X_train_scaled, y_co2_train)
            
            # Train site suitability classifier
            self.models['site_suitability'].fit(X_train_scaled, y_suitability)
            
            # Train ranking models
            self.models['intervention_ranking']['xgboost'].fit(X_train_scaled, y_ranking)
            self.models['intervention_ranking']['lightgbm'].fit(X_train_scaled, y_ranking)
            
            # Evaluate models
            co2_pred = self.models['co2_regression']['lasso'].predict(X_test_scaled)
            co2_mse = mean_squared_error(y_co2_test, co2_pred)
            
            suitability_pred = self.models['site_suitability'].predict(X_test_scaled)
            suitability_acc = accuracy_score(y_suitability, suitability_pred)
            
            print(f"✅ Models trained successfully!")
            print(f"   CO2 Regression MSE: {co2_mse:.4f}")
            print(f"   Site Suitability Accuracy: {suitability_acc:.4f}")
            
            # Save models
            self._save_models()
            
        except Exception as e:
            print(f"❌ Error training models: {e}")

# Global instance
ml_engine = ClimateMLEngine() 