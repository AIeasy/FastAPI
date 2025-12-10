
from fastapi import FastAPI
from datetime import datetime
import requests
import aiohttp
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="FastAPI GCP Pro")

# Define allowed origins for CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://launch-an-app.vercel.app"
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],    # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)
def weather_code_to_text(code):
    """Translate Open-Meteo weather code to human-readable text."""
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        80: "Rain showers", 81: "Heavy rain showers", 82: "Violent rain showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return codes.get(code, "Unknown")

@app.get("/")
async def root():
    """returning a welcome message at root."""
    return {"message": "Welcome to FastAPI"}

@app.get("/greet/{name}")
async def greet(name: str):
    """
    Greet the person
    
    Args:
        name (str): Name of the person
    """
    return {"message": f"Hello, {name}! Hows everything!"}

@app.get("/weather")
async def fetch_weather_today():
    """Fetch current weather data for Toronto using Open-Meteo API."""
    # Toronto coordinates: latitude=43.65107, longitude=-79.347015
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=43.65107&longitude=-79.347015&current_weather=true"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    # Extract and format
    current = data.get("current_weather", {})
    weather = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "weathercode": current.get("weathercode"),
        "condition": weather_code_to_text(current.get("weathercode")),
        "location": "Toronto, ON"
    }
    return weather

@app.get("/formulate")
async def process_input_evaluation_step_1(RFQ_ID: str,Supllier_Name:str,Supplier_ID:str,Supplier_Contack:str,Quote_status:str):
    """formulate the input to the standard format for evaluation agent"""
    input_data = {
        "RFQ_ID": RFQ_ID,
        "Supllier_Name": Supllier_Name,
        "Supplier_ID": Supplier_ID,
        "Supplier_Contack": Supplier_Contack,
        "Quote_status": Quote_status
    }
    return input_data
