"use client";
import { useRef, useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { fetchInterventions } from '../services/api';

// Use environment variable for Mapbox access token
mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN || '';

interface Intervention {
  id: number;
  name: string;
  description?: string;
  intervention_type: string;
  location_lat: number;
  location_lon: number;
  deployment_date: string;
  capacity_tonnes_co2: number;
  status: string;
  operator: string;
  cost_per_tonne?: number;
  technology_readiness_level?: number;
  verification_method?: string;
  expected_lifetime_years?: number;
  created_at: string;
  updated_at: string;
}

// CO2 data point interface
interface CO2DataPoint {
  position: [number, number];
  co2: number;
  elevation: number;
}

// Generate comprehensive mock CO₂ data for global coverage (optimized for globe)
const generateGlobalCO2Data = (): CO2DataPoint[] => {
  const data: CO2DataPoint[] = [];
  
  // Generate grid points across the globe with optimized spacing for globe view
  for (let lat = -75; lat <= 75; lat += 2.5) { // Slightly less dense for better performance
    for (let lon = -180; lon <= 180; lon += 2.5) {
      // Base CO₂ level
      let co2Level = 410;
      
      // Major urban/industrial centers with high CO₂
      const hotspots = [
        { lat: 40.7, lon: -74, intensity: 25, name: "New York" },
        { lat: 34.0, lon: -118, intensity: 22, name: "Los Angeles" },
        { lat: 51.5, lon: -0.1, intensity: 20, name: "London" },
        { lat: 35.7, lon: 139.7, intensity: 28, name: "Tokyo" },
        { lat: 39.9, lon: 116.4, intensity: 35, name: "Beijing" },
        { lat: 28.6, lon: 77.2, intensity: 30, name: "Delhi" },
        { lat: 31.2, lon: 121.5, intensity: 32, name: "Shanghai" },
        { lat: 55.8, lon: 37.6, intensity: 25, name: "Moscow" },
        { lat: 52.5, lon: 13.4, intensity: 18, name: "Berlin" },
        { lat: 48.9, lon: 2.3, intensity: 20, name: "Paris" },
        { lat: 41.9, lon: -87.6, intensity: 22, name: "Chicago" },
        { lat: 29.8, lon: -95.4, intensity: 28, name: "Houston" },
      ];
      
      // Apply hotspot effects
      hotspots.forEach(hotspot => {
        const distance = Math.sqrt(
          Math.pow((lat - hotspot.lat) * 111, 2) + 
          Math.pow((lon - hotspot.lon) * 111 * Math.cos(lat * Math.PI / 180), 2)
        );
        if (distance < 400) { // Slightly larger influence area for globe
          const effect = hotspot.intensity * Math.exp(-distance / 120);
          co2Level += effect;
        }
      });
      
      // Regional variations
      // Industrial regions (Northern hemisphere, mid-latitudes)
      if (lat > 30 && lat < 60) {
        co2Level += Math.random() * 10;
      }
      
      // Tropical deforestation areas
      if (Math.abs(lat) < 10 && ((lon > -80 && lon < -50) || (lon > 100 && lon < 150))) {
        co2Level += Math.random() * 15;
      }
      
      // Ocean areas - lower CO₂ (carbon sinks)
      const isOcean = (
        // Atlantic
        (lat > -60 && lat < 70 && lon > -60 && lon < 20) ||
        // Pacific  
        (lat > -60 && lat < 70 && ((lon > 120 && lon <= 180) || (lon >= -180 && lon < -80))) ||
        // Indian Ocean
        (lat > -60 && lat < 30 && lon > 20 && lon < 120)
      );
      
      if (isOcean) {
        co2Level -= Math.random() * 12;
      }
      
      // Forest areas - carbon sinks
      const isForest = (
        // Amazon
        (lat > -10 && lat < 10 && lon > -80 && lon < -50) ||
        // Congo Basin
        (lat > -5 && lat < 5 && lon > 10 && lon < 30) ||
        // Boreal forests
        (lat > 50 && lat < 70)
      );
      
      if (isForest) {
        co2Level -= Math.random() * 8;
      }
      
      // Add natural variation
      co2Level += (Math.random() - 0.5) * 8;
      
      // Ensure realistic bounds
      co2Level = Math.max(385, Math.min(450, co2Level));
      
      data.push({
        position: [lon, lat],
        co2: co2Level,
        elevation: Math.max(0, (co2Level - 400) * 5),
      });
    }
  }
  
  return data;
};

export default function OperatorIntelligenceDashboard() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [interventions, setInterventions] = useState<Intervention[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nasaPopup, setNasaPopup] = useState<{
    lng: number;
    lat: number;
    data: any;
  } | null>(null);
  const [nasaLoading, setNasaLoading] = useState(false);
  const [nasaError, setNasaError] = useState<string | null>(null);
  
  // Map view state for DeckGL - keep as numbers, DeckGL handles conversion
  const [viewState, setViewState] = useState({
    longitude: -74.006,
    latitude: 40.7128,
    zoom: 3,
    pitch: 0,
    bearing: 0
  });

  // Fetch interventions from your FastAPI backend
  useEffect(() => {
    setLoading(true);
    fetchInterventions()
      .then(data => setInterventions(data.interventions || data))
      .catch(err => setError(err.message || 'Failed to fetch interventions'))
      .finally(() => setLoading(false));
  }, []);

  // Initialize Mapbox map
  useEffect(() => {
    if (map.current || !mapContainer.current) return;
    
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/light-v11',
      center: [-74.006, 40.7128],
      zoom: 3,
    });

    map.current.addControl(new mapboxgl.NavigationControl());
    map.current.addControl(new mapboxgl.FullscreenControl());

    // Attach click handler to map
    map.current.on('click', (e) => {
      handleMapClick({ coordinate: [e.lngLat.lng, e.lngLat.lat] });
    });

    return () => {
      map.current?.remove();
    };
  }, []);

  // Add intervention markers
  useEffect(() => {
    if (!map.current || interventions.length === 0) return;

    // Clear existing markers
    const existingMarkers = document.querySelectorAll('.mapboxgl-marker');
    existingMarkers.forEach(marker => marker.remove());

    // Calculate bounds for all interventions
    const bounds = new mapboxgl.LngLatBounds();

    interventions.forEach((intervention) => {
      const { location_lon, location_lat, intervention_type, name, status } = intervention;

      // Create marker element
      const markerEl = document.createElement('div');
      markerEl.className = 'marker';
      markerEl.style.width = '25px';
      markerEl.style.height = '25px';
      markerEl.style.borderRadius = '50%';
      markerEl.style.backgroundColor = getMarkerColor(intervention_type);
      markerEl.style.border = '2px solid white';
      markerEl.style.cursor = 'pointer';
      markerEl.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
      markerEl.style.zIndex = '1000';

      // Create popup
      const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(`
        <div class="p-3">
          <h3 class="font-bold text-lg mb-2">${name}</h3>
          <p class="text-sm text-gray-600 mb-1"><strong>Type:</strong> ${intervention_type}</p>
          <p class="text-sm text-gray-600 mb-1"><strong>Status:</strong> ${status}</p>
          <p class="text-sm text-gray-600 mb-1"><strong>Capacity:</strong> ${intervention.capacity_tonnes_co2} tonnes CO₂</p>
          <p class="text-sm text-gray-600 mb-1"><strong>Operator:</strong> ${intervention.operator}</p>
          <p class="text-sm text-gray-600"><strong>Deployed:</strong> ${new Date(intervention.deployment_date).toLocaleDateString()}</p>
        </div>
      `);

      // Add marker to map
      new mapboxgl.Marker(markerEl)
        .setLngLat([location_lon, location_lat])
        .setPopup(popup)
        .addTo(map.current!);

      // Extend bounds to include this marker
      bounds.extend([location_lon, location_lat]);
    });

    // Fit map to show all markers
    if (!bounds.isEmpty()) {
      map.current.fitBounds(bounds, { padding: 50 });
    }
  }, [interventions]);

  // Handle map clicks for NASA data
  const handleMapClick = async (info: any) => {
    if (!info.coordinate) return;
    
    const [lng, lat] = info.coordinate;
    setNasaLoading(true);
    setNasaError(null);
    setNasaPopup(null);
    
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/climate-data/optimization?lat=${lat}&lon=${lng}`
      );
      const json = await res.json();
      if (json.success) {
        setNasaPopup({ lng: Number(lng), lat: Number(lat), data: json.data });
      } else {
        setNasaError(json.error || 'Failed to fetch NASA data');
      }
    } catch (err: any) {
      setNasaError(err.message || 'Failed to fetch NASA data');
    } finally {
      setNasaLoading(false);
    }
  };

  // Color function for CO₂ levels
  const getCO2Color = (co2Level: number): [number, number, number, number] => {
    if (co2Level > 420) return [255, 69, 58, 160]; // Red - Urgent
    if (co2Level > 410) return [255, 214, 10, 160]; // Yellow - Medium
    return [48, 209, 88, 160]; // Green - Low priority
  };

  const getMarkerColor = (interventionType: string): string => {
    const colors: { [key: string]: string } = {
      'biochar': '#8B4513',
      'DAC': '#0066CC', 
      'reforestation': '#228B22',
      'ocean_fertilization': '#4169E1',
      'enhanced_weathering': '#D2691E',
      'default': '#FF6B6B'
    };
    return colors[interventionType.toLowerCase()] || colors.default;
  };

  const getTotalCapacity = (): number => {
    return interventions.reduce((total, intervention) => total + intervention.capacity_tonnes_co2, 0);
  };

  const getInterventionsByType = (): { [key: string]: number } => {
    const typeCount: { [key: string]: number } = {};
    interventions.forEach(intervention => {
      typeCount[intervention.intervention_type] = (typeCount[intervention.intervention_type] || 0) + 1;
    });
    return typeCount;
  };

  return (
    <div className="min-h-screen bg-gray-50" style={{ position: 'relative' }}>
      {/* Loading and Error Overlays */}
      {loading && (
        <div style={{
          position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh',
          background: 'rgba(255,255,255,0.8)', zIndex: 10, display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
          <div className="text-xl">Loading interventions...</div>
        </div>
      )}
      {error && (
        <div style={{
          position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh',
          background: 'rgba(255,255,255,0.8)', zIndex: 10, display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
          <div className="text-xl text-red-600">Error: {error}</div>
        </div>
      )}

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Operator Intelligence Dashboard
              </h1>
              <p className="text-sm text-gray-600">
                Climate Intervention Deployment Overview
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-green-600">
                {getTotalCapacity().toLocaleString()} tonnes CO₂
              </div>
              <div className="text-sm text-gray-600">Total Removal Capacity</div>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex space-x-8">
            <div>
              <span className="text-sm font-medium text-gray-500">Total Interventions:</span>
              <span className="ml-2 text-sm font-semibold text-gray-900">{interventions.length}</span>
            </div>
            {Object.entries(getInterventionsByType()).map(([type, count]) => (
              <div key={type}>
                <span className="text-sm font-medium text-gray-500">{type}:</span>
                <span className="ml-2 text-sm font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Map Container with DeckGL */}
      <div className="relative flex-1">
        <div ref={mapContainer} className="absolute inset-0 w-full h-[calc(100vh-140px)]" />
      </div>

      {/* Comprehensive Legend */}
      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-4 max-w-xs">
        <h3 className="font-semibold text-sm mb-3">Climate Intervention Intelligence</h3>
        
        <div className="mb-4">
          <h4 className="font-medium text-xs mb-2 text-gray-700">CO₂ Concentration Levels</h4>
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <span className="text-xs text-gray-700">High (&gt;420 ppm) - Urgent Action</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <span className="text-xs text-gray-700">Medium (410-420 ppm) - Monitor</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="text-xs text-gray-700">Low (&lt;410 ppm) - Stable</span>
            </div>
          </div>
        </div>
        
        {Object.keys(getInterventionsByType()).length > 0 && (
          <div>
            <h4 className="font-medium text-xs mb-2 text-gray-700">Active Interventions</h4>
            <div className="space-y-1">
              {Object.entries(getInterventionsByType()).map(([type, count]) => (
                <div key={`legend-${type}`} className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full border border-white"
                    style={{ backgroundColor: getMarkerColor(type) }}
                  />
                  <span className="text-xs text-gray-700">{type} ({count})</span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        <div className="mt-3 pt-3 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            Click anywhere for NASA climate analysis
          </p>
        </div>
      </div>

      {/* NASA Data Popup */}
      {nasaPopup && (
        <div
          className="absolute z-50 bg-white rounded-lg shadow-xl p-6 border"
          style={{
            left: '50%',
            top: 120,
            transform: 'translateX(-50%)',
            minWidth: 360,
            maxWidth: 420,
          }}
        >
          <button
            className="absolute top-3 right-3 text-gray-400 hover:text-gray-700 text-xl font-bold"
            onClick={() => setNasaPopup(null)}
          >
            ×
          </button>
          
          <div className="mb-4">
            <h3 className="font-bold text-lg mb-1 text-gray-900">NASA Climate Intelligence</h3>
            <p className="text-sm text-gray-500">
              {Number(nasaPopup.lat).toFixed(4)}, {Number(nasaPopup.lng).toFixed(4)}
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <div className="text-xs text-blue-600 font-medium">CO₂ Level</div>
              <div className="text-lg font-bold text-blue-900">
                {nasaPopup.data.current_conditions?.co2?.co2_concentration || 'N/A'} ppm
              </div>
            </div>
            <div className="bg-orange-50 p-3 rounded-lg">
              <div className="text-xs text-orange-600 font-medium">Temperature</div>
              <div className="text-lg font-bold text-orange-900">
                {nasaPopup.data.current_conditions?.temperature?.temperature || 'N/A'}°C
              </div>
            </div>
          </div>
          
          <div className="mb-4">
            <h4 className="font-semibold text-sm mb-2 text-gray-800">Intervention Analysis</h4>
            <div className="bg-gray-50 p-3 rounded-lg space-y-1">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Optimal Type:</span>
                <span className="text-sm font-medium text-gray-900">
                  {nasaPopup.data.intervention_recommendations?.optimal_intervention_type || 'N/A'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Priority:</span>
                <span className={`text-sm font-medium ${
                  nasaPopup.data.intervention_recommendations?.deployment_priority === 'high' ? 'text-red-600' :
                  nasaPopup.data.intervention_recommendations?.deployment_priority === 'medium' ? 'text-yellow-600' : 'text-green-600'
                }`}>
                  {nasaPopup.data.intervention_recommendations?.deployment_priority || 'N/A'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Expected Impact:</span>
                <span className="text-sm font-medium text-gray-900">
                  {nasaPopup.data.intervention_recommendations?.expected_impact || 'N/A'}
                </span>
              </div>
            </div>
          </div>
          
          <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium">
            Analyze Site
          </button>
        </div>
      )}
      
      {/* Loading and Error States for NASA */}
      {nasaLoading && (
        <div className="absolute z-50 left-1/2 top-32 transform -translate-x-1/2 bg-white rounded-lg shadow-lg p-4">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="text-sm text-gray-700">Loading NASA climate data...</span>
          </div>
        </div>
      )}
      
      {nasaError && (
        <div className="absolute z-50 left-1/2 top-32 transform -translate-x-1/2 bg-red-50 border border-red-200 text-red-700 rounded-lg shadow-lg p-4 max-w-sm">
          <div className="flex justify-between items-start">
            <span className="text-sm">Error: {nasaError}</span>
            <button 
              className="ml-3 text-red-400 hover:text-red-600"
              onClick={() => setNasaError(null)}
            >
              ×
            </button>
          </div>
        </div>
      )}
    </div>
  );
}