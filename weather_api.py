import requests
import shutil
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

API_KEY = "B8RlZtMZggBNQmzBoxH9aROhowLuyBSQ7dJFyNz8"

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
def get_sat_image(lat: float, long: float, key: str):
    api_url = (
        f"https://api.nasa.gov/planetary/earth/imagery"
        f"?lon={long}&lat={lat}&api_key={key}"
    )
    img = requests.get(api_url, stream=True)
    with open('img.png', 'wb') as f:
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, f)
    return 'img.png'
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

@app.get("/satellite")
def get_satellite_image(
    lat: float = Query(...),
    long: float = Query(...)
):
    try:
        image_path = get_sat_image(lat, long, API_KEY)
        return FileResponse(image_path, media_type="image/png", filename="satellite.png")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

