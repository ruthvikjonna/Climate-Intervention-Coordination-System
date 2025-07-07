## Core API Endpoints

### Interventions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/interventions/` | Create a new intervention (DAC, biochar, etc.) |
| `GET` | `/api/v1/interventions/` | List all interventions |
| `GET` | `/api/v1/interventions/{id}` | Get details of a specific intervention |
| `PUT` | `/api/v1/interventions/{id}` | Update a specific intervention |
| `DELETE` | `/api/v1/interventions/{id}` | Delete a specific intervention |
| `GET` | `/api/v1/interventions/operator/{operator_id}` | Filter interventions by operator |
| `GET` | `/api/v1/interventions/type/{intervention_type}` | Filter interventions by type |
| `GET` | `/api/v1/interventions/status/{status}` | Filter interventions by status |
| `GET` | `/api/v1/interventions/stats/total-scale` | Total scale of all interventions |
| `GET` | `/api/v1/interventions/stats/scale-by-type` | Scale of interventions by type |

### Satellite Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/satellite-data/` | Add satellite-derived dataset |
| `GET` | `/api/v1/satellite-data/` | List all satellite data entries |
| `GET` | `/api/v1/satellite-data/{id}` | View specific satellite data |
| `PUT` | `/api/v1/satellite-data/{id}` | Update satellite data entry |
| `DELETE` | `/api/v1/satellite-data/{id}` | Delete satellite data entry |
| `GET` | `/api/v1/satellite-data/grid-cell/{grid_cell_id}` | View satellite data for a grid cell |
| `GET` | `/api/v1/satellite-data/satellite/{satellite_id}` | Filter data by satellite |
| `GET` | `/api/v1/satellite-data/time-range/` | Filter data by date range |
| `GET` | `/api/v1/satellite-data/grid-cell/{grid_cell_id}/latest` | Get most recent reading for grid cell |
| `GET` | `/api/v1/satellite-data/statistics/` | Aggregated satellite stats |

### Intervention Impacts
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/intervention-impacts/` | Submit impact report |
| `GET` | `/api/v1/intervention-impacts/` | List all impact entries |
| `GET` | `/api/v1/intervention-impacts/{id}` | View specific impact record |
| `PUT` | `/api/v1/intervention-impacts/{id}` | Update impact data |
| `DELETE` | `/api/v1/intervention-impacts/{id}` | Delete impact record |
| `GET` | `/api/v1/intervention-impacts/intervention/{intervention_id}` | View impacts for a given intervention |
| `GET` | `/api/v1/intervention-impacts/grid-cell/{grid_cell_id}` | View impacts at a location |
| `GET` | `/api/v1/intervention-impacts/effectiveness-range/` | Filter impacts by performance range |
| `GET` | `/api/v1/intervention-impacts/best-performing/` | Top-ranked interventions by effectiveness |
| `GET` | `/api/v1/intervention-impacts/statistics/` | Aggregate impact metrics |

### Optimization Results
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/optimization-results/` | Submit optimization result |
| `GET` | `/api/v1/optimization-results/` | List all results |
| `GET` | `/api/v1/optimization-results/{id}` | View specific optimization result |
| `PUT` | `/api/v1/optimization-results/{id}` | Update optimization result |
| `DELETE` | `/api/v1/optimization-results/{id}` | Delete result |
| `GET` | `/api/v1/optimization-results/operator/{operator_id}` | Filter by operator |
| `GET` | `/api/v1/optimization-results/grid-cell/{grid_cell_id}` | Filter by grid cell |
| `GET` | `/api/v1/optimization-results/type/{optimization_type}` | Filter by optimization type |
| `GET` | `/api/v1/optimization-results/algorithm/{algorithm}` | Filter by algorithm used |
| `GET` | `/api/v1/optimization-results/status/{status}` | Filter by result status |
| `GET` | `/api/v1/optimization-results/best-performing/` | Top optimization runs |
| `GET` | `/api/v1/optimization-results/statistics/` | Aggregate stats |

### Data Sources
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/data-sources/` | Register a data source |
| `GET` | `/api/v1/data-sources/` | List all sources |
| `GET` | `/api/v1/data-sources/{id}` | View a specific source |
| `PUT` | `/api/v1/data-sources/{id}` | Update source metadata |
| `DELETE` | `/api/v1/data-sources/{id}` | Delete a source |
| `PUT` | `/api/v1/data-sources/{id}/status` | Toggle source status |
| `GET` | `/api/v1/data-sources/type/{type}` | Filter by source type |
| `GET` | `/api/v1/data-sources/provider/{provider}` | Filter by data provider |
| `GET` | `/api/v1/data-sources/active/` | List active sources only |
| `GET` | `/api/v1/data-sources/auth/{requires_auth}` | Filter by auth requirement |
| `GET` | `/api/v1/data-sources/frequency/{frequency}` | Filter by update frequency |
| `GET` | `/api/v1/data-sources/search/{term}` | Search sources |
| `GET` | `/api/v1/data-sources/statistics/` | Aggregate usage stats |

### Climate Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/climate-data/` | Full climate dataset |
| `GET` | `/api/v1/climate-data/co2` | CO₂-specific data |
| `GET` | `/api/v1/climate-data/temperature` | Temperature metrics |
| `GET` | `/api/v1/climate-data/biomass` | Biomass data |
| `GET` | `/api/v1/climate-data/historical` | Historical records |
| `GET` | `/api/v1/climate-data/optimization` | Optimization-ready data |
| `GET` | `/api/v1/climate-data/satellite-imagery` | Remote sensing imagery |

### Meta & Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API root |
| `GET` | `/health` | API health check |
