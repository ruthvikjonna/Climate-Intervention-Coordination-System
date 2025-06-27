"use client";
import { useRef, useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

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

  // Fetch interventions from your FastAPI backend
  useEffect(() => {
    const fetchInterventions = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/interventions/');
        if (!response.ok) {
          throw new Error('Failed to fetch interventions');
        }
        const data = await response.json();
        setInterventions(data.interventions || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch interventions');
      } finally {
        setLoading(false);
      }
    };

    fetchInterventions();
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
    </div>
  );
}
