from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from weather import get_weather_by_location
from crop_engine import recommend_crops, get_crop_guidance
from chat import chat_with_farmer
from database import init_db, save_session, get_session

app = FastAPI(title="AgroNova API", version="1.0.0")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# ─── MODELS ──────────────────────────────────────────────────────────────────

class WeatherRequest(BaseModel):
    location: str
    language: str = "english"

class CropRequest(BaseModel):
    location: str
    temperature: float
    rainfall: float
    humidity: float
    soil_type: str
    water_level: str
    language: str = "english"

class CropSelectRequest(BaseModel):
    crop_key: str
    language: str = "english"
    area_hectares: float = 1.0

class ChatRequest(BaseModel):
    message: str
    language: str = "english"
    context: dict = {}
    history: List[dict] = []

# ─── TRANSLATIONS ─────────────────────────────────────────────────────────────

TRANSLATIONS = {
    "english": {
        "welcome": "Welcome to AgroNova - Smart Farming for Smart India",
        "select_language": "Select your language",
        "enter_location": "Enter your village/city name",
        "fetching_weather": "Fetching weather data for your location...",
        "select_soil": "Select your soil type",
        "select_water": "Select water availability",
        "analyzing": "AI is analyzing your field conditions...",
        "top_crops": "Top 3 Recommended Crops",
        "select_crop": "Select a crop to get detailed guidance",
        "weather_fetched": "Weather data fetched successfully",
        "location_not_found": "Location not found. Please try a nearby city.",
    },
    "hindi": {
        "welcome": "AgroNova में आपका स्वागत है - स्मार्ट भारत के लिए स्मार्ट खेती",
        "select_language": "अपनी भाषा चुनें",
        "enter_location": "अपने गांव/शहर का नाम दर्ज करें",
        "fetching_weather": "आपके स्थान के लिए मौसम डेटा प्राप्त किया जा रहा है...",
        "select_soil": "मिट्टी का प्रकार चुनें",
        "select_water": "पानी की उपलब्धता चुनें",
        "analyzing": "AI आपके खेत की स्थितियों का विश्लेषण कर रहा है...",
        "top_crops": "शीर्ष 3 अनुशंसित फसलें",
        "select_crop": "विस्तृत मार्गदर्शन के लिए एक फसल चुनें",
        "weather_fetched": "मौसम डेटा सफलतापूर्वक प्राप्त किया गया",
        "location_not_found": "स्थान नहीं मिला। कृपया नजदीकी शहर आज़माएं।",
    },
    "marathi": {
        "welcome": "AgroNova मध्ये आपले स्वागत आहे - स्मार्ट भारतासाठी स्मार्ट शेती",
        "select_language": "आपली भाषा निवडा",
        "enter_location": "आपल्या गाव/शहराचे नाव टाका",
        "fetching_weather": "आपल्या ठिकाणाचा हवामान डेटा मिळवत आहे...",
        "select_soil": "मातीचा प्रकार निवडा",
        "select_water": "पाण्याची उपलब्धता निवडा",
        "analyzing": "AI आपल्या शेताच्या परिस्थितीचे विश्लेषण करत आहे...",
        "top_crops": "शीर्ष 3 शिफारस केलेली पिके",
        "select_crop": "सविस्तर मार्गदर्शनासाठी एक पीक निवडा",
        "weather_fetched": "हवामान डेटा यशस्वीरित्या मिळाला",
        "location_not_found": "ठिकाण सापडले नाही. कृपया जवळचे शहर वापरा.",
    }
}

# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return FileResponse("../frontend/index.html")

@app.get("/api/translations/{language}")
def get_translations(language: str):
    lang = language.lower()
    if lang not in TRANSLATIONS:
        lang = "english"
    return {"language": lang, "translations": TRANSLATIONS[lang]}

@app.post("/api/weather")
def fetch_weather(req: WeatherRequest):
    """Fetch real weather data for a location"""
    result = get_weather_by_location(req.location)
    if result["success"]:
        return result
    else:
        lang = req.language.lower()
        msg = TRANSLATIONS.get(lang, TRANSLATIONS["english"])["location_not_found"]
        raise HTTPException(status_code=404, detail=msg)

@app.post("/api/recommend-crops")
def recommend(req: CropRequest):
    """AI crop recommendation based on field data"""
    crops = recommend_crops(
        soil_type=req.soil_type,
        temperature=req.temperature,
        rainfall=req.rainfall,
        humidity=req.humidity,
        water_level=req.water_level,
        language=req.language
    )
    # Save session to DB
    session_data = {
        "location": req.location,
        "temperature": req.temperature,
        "rainfall": req.rainfall,
        "soil_type": req.soil_type,
        "water_level": req.water_level,
        "recommended_crops": [c["key"] for c in crops]
    }
    session_id = save_session(session_data)
    return {"session_id": session_id, "crops": crops}

@app.post("/api/crop-guidance")
def crop_guidance(req: CropSelectRequest):
    """Get detailed guidance for selected crop"""
    guidance = get_crop_guidance(req.crop_key, req.language, req.area_hectares)
    if not guidance:
        raise HTTPException(status_code=404, detail="Crop not found")
    return guidance

@app.post("/api/chat")
def chat(req: ChatRequest):
    """AI chat with farmer in their language"""
    response = chat_with_farmer(
        message=req.message,
        language=req.language,
        context=req.context,
        history=req.history
    )
    return {"reply": response}

@app.get("/api/health")
def health():
    return {"status": "AgroNova API is running! 🌱"}
