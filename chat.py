import os
import requests
import json

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPTS = {
    "english": """You are AgroNova's AI farming assistant. You help Indian farmers with crop advice.
Keep responses SHORT, SIMPLE and PRACTICAL — farmers need clear actionable advice.
Max 3-4 sentences per response. Use simple English.
Focus on: crops, soil, weather, fertilizers, irrigation, pest control, market prices.
If asked about something not related to farming, politely redirect to farming topics.
Always be encouraging and respectful to farmers.""",

    "hindi": """आप AgroNova के AI कृषि सहायक हैं। आप भारतीय किसानों को फसल की सलाह देते हैं।
जवाब छोटे, सरल और व्यावहारिक रखें — किसानों को स्पष्ट सलाह चाहिए।
प्रति उत्तर अधिकतम 3-4 वाक्य। सरल हिंदी में लिखें।
फोकस: फसलें, मिट्टी, मौसम, खाद, सिंचाई, कीट नियंत्रण, बाजार भाव।
हमेशा किसानों के प्रति सम्मानजनक और प्रोत्साहनजनक रहें।""",

    "marathi": """तुम्ही AgroNova चे AI शेती सहाय्यक आहात. तुम्ही भारतीय शेतकऱ्यांना पीक सल्ला देता.
उत्तरे छोटी, सोपी आणि व्यावहारिक ठेवा — शेतकऱ्यांना स्पष्ट सल्ला हवा.
प्रति उत्तर जास्तीत जास्त 3-4 वाक्ये. सोप्या मराठीत लिहा.
फोकस: पिके, माती, हवामान, खते, सिंचन, कीड नियंत्रण, बाजार भाव.
नेहमी शेतकऱ्यांशी आदराने आणि प्रोत्साहनाने बोला."""
}

def chat_with_farmer(message: str, language: str = "english",
                     context: dict = {}, history: list = []) -> str:
    """
    Chat with farmer using Claude AI.
    Falls back to rule-based responses if no API key.
    """
    lang = language.lower()
    if lang not in SYSTEM_PROMPTS:
        lang = "english"

    if not ANTHROPIC_API_KEY:
        return get_rule_based_response(message, lang, context)

    try:
        # Build context string
        context_str = ""
        if context:
            context_str = f"\n\nFarmer's current situation: {json.dumps(context, ensure_ascii=False)}"

        system = SYSTEM_PROMPTS[lang] + context_str

        # Build messages with history
        messages = []
        for h in history[-6:]:  # Keep last 6 messages
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": message})

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 300,
                "system": system,
                "messages": messages
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            return data["content"][0]["text"]
        else:
            return get_rule_based_response(message, lang, context)

    except Exception:
        return get_rule_based_response(message, lang, context)


def get_rule_based_response(message: str, language: str, context: dict) -> str:
    """
    Simple rule-based fallback responses when no API key.
    """
    msg = message.lower()

    responses = {
        "english": {
            "fertilizer": "For most crops, use NPK fertilizer. Apply urea in splits — 50% at sowing and 50% at 30 days. Always follow soil test recommendations for best results.",
            "water": "Water your crop based on soil moisture. Most crops need water every 7-10 days in dry weather. Check soil 2 inches deep — if dry, irrigate.",
            "pest": "For pest control, first try neem-based sprays as they are safe and cheap. If severe, consult your local agriculture officer for recommended pesticides.",
            "price": "Current market prices vary by region. Check your nearest mandi or use the eNAM app for live prices. Sell when prices are high, usually after festivals.",
            "soil": "Improve your soil by adding organic matter like compost or farmyard manure every year. Good soil means better yield and less fertilizer needed.",
            "default": "That's a great question! For the best advice on your specific situation, I recommend consulting your local Krishi Vigyan Kendra (KVK). They provide free expert advice to farmers."
        },
        "hindi": {
            "fertilizer": "अधिकांश फसलों के लिए NPK खाद का उपयोग करें। यूरिया को दो भागों में दें — 50% बुवाई पर और 50% 30 दिनों पर। सर्वोत्तम परिणामों के लिए मिट्टी परीक्षण की सलाह का पालन करें।",
            "water": "मिट्टी की नमी के आधार पर फसल को पानी दें। अधिकांश फसलों को सूखे मौसम में हर 7-10 दिनों में पानी चाहिए।",
            "pest": "कीट नियंत्रण के लिए पहले नीम आधारित स्प्रे आज़माएं। अगर गंभीर हो, तो स्थानीय कृषि अधिकारी से सलाह लें।",
            "price": "बाजार भाव क्षेत्र के अनुसार बदलते हैं। लाइव भाव के लिए eNAM ऐप या नजदीकी मंडी देखें।",
            "default": "यह एक अच्छा सवाल है! अपनी विशिष्ट स्थिति के लिए, कृपया अपने स्थानीय कृषि विज्ञान केंद्र (KVK) से सलाह लें।"
        },
        "marathi": {
            "fertilizer": "बहुतेक पिकांसाठी NPK खत वापरा. युरिया दोन हप्त्यांत द्या — 50% पेरणीच्या वेळी आणि 50% 30 दिवसांनी. माती परीक्षण शिफारशींचे पालन करा.",
            "water": "जमिनीतील ओलाव्यानुसार पिकाला पाणी द्या. बहुतेक पिकांना दुष्काळी हवामानात दर 7-10 दिवसांनी पाणी लागते.",
            "pest": "कीड नियंत्रणासाठी प्रथम निंबोळी आधारित फवारणी वापरा. गंभीर असल्यास स्थानिक कृषी अधिकाऱ्याचा सल्ला घ्या.",
            "price": "बाजारभाव प्रदेशानुसार बदलतो. थेट भावासाठी eNAM अॅप किंवा जवळची बाजारसमिती पहा.",
            "default": "हा एक चांगला प्रश्न आहे! तुमच्या विशिष्ट परिस्थितीसाठी, कृपया जवळच्या कृषी विज्ञान केंद्राशी (KVK) संपर्क करा."
        }
    }

    r = responses.get(language, responses["english"])

    if any(w in msg for w in ["fertilizer", "khad", "खाद", "खत", "urea", "npk"]):
        return r.get("fertilizer", r["default"])
    elif any(w in msg for w in ["water", "irrigation", "pani", "पानी", "पाणी", "sinchane"]):
        return r.get("water", r["default"])
    elif any(w in msg for w in ["pest", "insect", "keet", "कीट", "किडी", "disease"]):
        return r.get("pest", r["default"])
    elif any(w in msg for w in ["price", "bhav", "भाव", "market", "mandi", "मंडी"]):
        return r.get("price", r["default"])
    elif any(w in msg for w in ["soil", "mitti", "माती", "मिट्टी"]):
        return r.get("soil", r["default"])
    else:
        return r["default"]
