import requests
from requests.auth import HTTPBasicAuth
import netCDF4 as nc
import numpy as np
from datetime import datetime, timedelta
import os

NASA_USERNAME = os.getenv("NASA_EARTHDATA_USERNAME")
NASA_PASSWORD = os.getenv("NASA_EARTHDATA_PASSWORD")

MERRA2_BASE_URL = "https://goldsmr5.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXAER.5.12.4"

# MERRA-2 file naming convention: MERRA2_400.tavg1_2d_aer_Nx.YYYYMMDD.nc4
# We'll use collection 400 (post-2000)
def get_merra2_url(date: datetime) -> str:
    year = date.year
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    fname = f"MERRA2_400.tavg1_2d_aer_Nx.{year}{month}{day}.nc4"
    return f"{MERRA2_BASE_URL}/{year}/{month}/{fname}"

def fetch_merra2_file(date: datetime, max_days_back: int = 7) -> str:
    """
    Try to fetch the NetCDF file for the given date, falling back up to max_days_back days.
    Returns the local filename if successful, else raises Exception.
    """
    for i in range(max_days_back):
        try_date = date - timedelta(days=i)
        url = get_merra2_url(try_date)
        print(f"Trying NASA MERRA-2 URL: {url}")
        response = requests.get(url, auth=HTTPBasicAuth(NASA_USERNAME, NASA_PASSWORD))
        if response.status_code == 200:
            local_file = f"/tmp/merra2_{try_date.strftime('%Y%m%d')}.nc4"
            with open(local_file, "wb") as f:
                f.write(response.content)
            return local_file
    
    raise Exception(f"Could not fetch MERRA-2 data for {date.date()} or previous {max_days_back} days.")

def parse_merra2_file(nc_file: str):
    ds = nc.Dataset(nc_file)
    # Print available variables for debugging
    print("Variables in file:", ds.variables.keys())
    # CO2 is often 'CO2' or 'co2', temperature is 'T' or 't'
    co2 = ds.variables.get('CO2')
    temp = ds.variables.get('T')
    lats = ds.variables.get('lat')[:]
    lons = ds.variables.get('lon')[:]
    # For demo, return mean values (can return full grid for heatmap)
    co2_data = float(np.mean(co2[:])) if co2 is not None else None
    temp_data = float(np.mean(temp[:])) if temp is not None else None
    return {
        "co2_mean": co2_data,
        "temperature_mean": temp_data,
        "lat": lats.tolist(),
        "lon": lons.tolist(),
        # Optionally, return full grid data for heatmap overlays
        # "co2_grid": co2[:].tolist() if co2 is not None else None,
        # "temperature_grid": temp[:].tolist() if temp is not None else None,
    }

def get_climate_data(date: datetime = None):
    if date is None:
        date = datetime.utcnow()
    nc_file = fetch_merra2_file(date)
    return parse_merra2_file(nc_file) 