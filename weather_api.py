import requests
import shutil
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

def call_forecast(lat: float, long: float):
    api_url = f"https://api.weather.gov/points/{lat},{long}"
    response = requests.get(api_url).json()
    
    forecast_hourly = response['properties']['forecast']
    forecasts = requests.get(forecast_hourly).json()
    return forecasts['properties']
def call_alert(lat:float,long:float):
    api_url = f"https://api.weather.gov/points/{lat},{long}"
    response = requests.get(api_url).json()
    
    
    forecast_hourly = response['properties']['fireWeatherZone']
    forecasts = requests.get(forecast_hourly).json()
    return forecasts['properties']

@app.get("/alert")
def get_alerts(lat:float = Query(...) , long:float = Query(...)):
    try:
        alert_data = call_alert(lat,long)
        return JSONResponse(content = alert_data)
    except Exception as e:
        return JSONResponse(content = {"error": str(e)}, status_code = 500)
@app.get("/forecast")
def get_forecast(lat: float = Query(...), long: float = Query(...)):
    try:
        forecast_data = call_forecast(lat, long)
        return JSONResponse(content=forecast_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

