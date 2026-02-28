# 🌱 AgroNova — Smart Farming for Smart India

AI-powered crop recommendation system with multilingual support (English, Hindi, Marathi).

## 🚀 How to Run on GitHub Codespaces

### Step 1 — Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys (optional for demo)
```

### Step 3 — Start the backend server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4 — Open the app
- Codespaces will show a popup: **"Open in Browser"** → Click it!
- Or go to the **Ports** tab → click the link for port 8000

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

## 🔑 API Keys (Optional)
- **OpenWeatherMap** (free): https://openweathermap.org/api — for real weather
- **Anthropic Claude** (free tier): https://console.anthropic.com — for AI chat

Without API keys, the app runs in **demo mode** with sample data.

## ⚡ AMD Integration
- Backend built to run on **AMD EPYC** cloud servers
- AI model ready for **AMD ROCm** + PyTorch training
- Edge deployment via **AMD Ryzen Embedded**

## 🏆 AMD Slingshot Hackathon
Built for AMD Slingshot Ideathon — "Human Imagination Built with AI"
