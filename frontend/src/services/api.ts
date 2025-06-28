const API_BASE = 'http://localhost:8000/api/v1';

export const fetchInterventions = async () => {
  const response = await fetch(`${API_BASE}/interventions/`);
  if (!response.ok) throw new Error('Failed to fetch interventions');
  return response.json();
};

export const fetchOperators = async () => {
  const response = await fetch(`${API_BASE}/operators/`);
  if (!response.ok) throw new Error('Failed to fetch operators');
  return response.json();
};

export const fetchSatelliteData = async () => {
  const response = await fetch(`${API_BASE}/satellite-data/`);
  if (!response.ok) throw new Error('Failed to fetch satellite data');
  return response.json();
}; 