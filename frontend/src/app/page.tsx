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

  // Fetch interventions from your FastAPI backend
  useEffect(() => {
    setLoading(true);
    fetchInterventions()
      .then(data => setInterventions(data.interventions || data))
      .catch(err => setError(err.message || 'Failed to fetch interventions'))
      .finally(() => setLoading(false));
  }, []);

  // Initialize map
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

    return () => {
      map.current?.remove();
    };
  }, []);

  // Add markers when interventions data is loaded
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

  useEffect(() => {
    if (map.current) {
      map.current.on('click', async (e) => {
        const { lng, lat } = e.lngLat;
        setNasaLoading(true);
        setNasaError(null);
        setNasaPopup(null);
        try {
          const res = await fetch(
            `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/climate-data/optimization?lat=${lat}&lon=${lng}`
          );
          const json = await res.json();
          if (json.success) {
            setNasaPopup({ lng, lat, data: json.data });
          } else {
            setNasaError(json.error || 'Failed to fetch NASA data');
          }
        } catch (err: any) {
          setNasaError(err.message || 'Failed to fetch NASA data');
        } finally {
          setNasaLoading(false);
        }
      });
    }
  }, []);

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

  const getTotalCapacity = () => {
    return interventions.reduce((total, intervention) => total + intervention.capacity_tonnes_co2, 0);
  };

  const getInterventionsByType = () => {
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

      {/* Map Container */}
      <div className="relative flex-1">
        <div ref={mapContainer} className="w-full h-[calc(100vh-140px)]" />
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-4">
        <h3 className="font-semibold text-sm mb-2">Intervention Types</h3>
        <div className="space-y-1">
          {Object.entries(getInterventionsByType()).map(([type, count]) => (
            <div key={type} className="flex items-center space-x-2">
              <div 
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: getMarkerColor(type) }}
              ></div>
              <span className="text-xs text-gray-700">{type} ({count})</span>
            </div>
          ))}
        </div>
      </div>

      {nasaPopup && (
        <div
          className="absolute z-50 bg-white rounded-lg shadow-lg p-4"
          style={{
            left: '50%',
            top: 120,
            transform: 'translateX(-50%)',
            minWidth: 320,
            maxWidth: 400,
          }}
        >
          <button
            className="absolute top-2 right-2 text-gray-400 hover:text-gray-700"
            onClick={() => setNasaPopup(null)}
          >
            ×
          </button>
          <h3 className="font-bold text-lg mb-2">NASA Climate Data</h3>
          <div className="text-sm text-gray-700">
            <div><b>Location:</b> {nasaPopup.lat.toFixed(4)}, {nasaPopup.lng.toFixed(4)}</div>
            <div><b>CO₂:</b> {nasaPopup.data.current_conditions?.co2?.co2_concentration} ppm</div>
            <div><b>Temperature:</b> {nasaPopup.data.current_conditions?.temperature?.temperature}°C</div>
            <div><b>Biomass:</b> {nasaPopup.data.current_conditions?.biomass?.biomass_density} t/ha</div>
            <div><b>Optimal Intervention:</b> {nasaPopup.data.intervention_recommendations?.optimal_intervention_type}</div>
            <div><b>Priority:</b> {nasaPopup.data.intervention_recommendations?.deployment_priority}</div>
            <div><b>Expected Impact:</b> {nasaPopup.data.intervention_recommendations?.expected_impact}</div>
          </div>
        </div>
      )}
      {nasaLoading && (
        <div className="absolute z-50 left-1/2 top-32 transform -translate-x-1/2 bg-white rounded shadow p-4">
          <span>Loading NASA data...</span>
        </div>
      )}
      {nasaError && (
        <div className="absolute z-50 left-1/2 top-32 transform -translate-x-1/2 bg-red-100 text-red-700 rounded shadow p-4">
          <span>Error: {nasaError}</span>
          <button className="ml-2 text-gray-500" onClick={() => setNasaError(null)}>×</button>
        </div>
      )}
    </div>
  );
}
