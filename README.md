# 🌱 AgroNova — Smart Farming for Smart India

AI-powered crop recommendation system with multilingual support (English, Hindi, Marathi).

## 🚀 How to Open

Website:
https://agronova-0-1-1.onrender.com

Topics:
fastapi python agriculture india ai farming crop-recommendation multilingual

## 📁 Project Structure
```
agronova/
├── backend/
│   ├── main.py          ← FastAPI server (all routes)
│   ├── crop_engine.py   ← AI crop recommendation logic
│   ├── weather.py       ← OpenWeatherMap API integration
│   ├── chat.py          ← Claude AI chat (multilingual)
│   ├── database.py      ← SQLite database
│   └── requirements.txt
├── frontend/
│   └── index.html       ← Full UI (connects to backend)
├── .env.example
└── README.md
```

## 🌐 Features
- ✅ Language selection: English, Hindi, Marathi
- ✅ Location input → auto-fetch weather (temp, rain, humidity)
- ✅ Soil type + water level input
- ✅ AI crop recommendation (top 3 with match %)
- ✅ Complete crop guidance (seeds, pre/post planting, fertilizers)
- ✅ Farm calculator (cost, yield, profit, ROI)
- ✅ AI chat with farmer in their language
- ✅ SQLite database saves all sessions

## 🔑 API Keys 
- **OpenWeatherMap** : https://openweathermap.org/api — for real weather
- **Anthropic Claude** : https://console.anthropic.com — for AI chat

Without API keys, the app runs in **demo mode** with sample data.

## ⚡ AMD Integration
- Backend built to run on **AMD EPYC** cloud servers
- AI model ready for **AMD ROCm** + PyTorch training
- Edge deployment via **AMD Ryzen Embedded**


