import os, requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

CITY_COORDS = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014),
    "인천": (37.4563, 126.7320),
    "광주": (35.1596, 126.8372),
    "도쿄": (35.6762, 139.6503),
    "뉴욕": (40.7128, -74.0060),
    "런던": (51.5074, -0.1278),
    "베이징": (39.9042, 116.4074),
    "파리": (48.8566, 2.3522),
}

WMO_CODES = {
    0: "맑음", 1: "대체로 맑음", 2: "부분적으로 흐림", 3: "흐림",
    45: "안개", 48: "짙은 안개", 51: "가벼운 이슬비", 53: "이슬비", 
    61: "약한 비", 63: "비", 65: "강한 비", 71: "약한 눈", 
    73: "눈", 75: "강한 눈", 80: "소나기", 95: "뇌우"
}

def get_current_weather(city: str) -> str:
    """도시의 실시간 날씨 정보를 Opne-Meteo API를 통해 가져옵니다.
    
    Args:
        city: 날씨를 가져올 도시 이름(예: 서울, 부산, 대구)
        
    Returns:
        현재 기온, 풍속, 날씨 상태를 담은 문자열
    """
    
    city = city.strip()
    coords = CITY_COORDS.get(city)
    if not coords:
        available = ", ".join(CITY_COORDS.keys())
        return f"{city}의 날씨 정보를 가져올 수 없습니다. 지원되는 도시: {', '.join(CITY_COORDS.keys())}"
    
    lat, lon = coords
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_temperature_2m,windspeed_10m,weathercode"
    )
    
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        current = resp.json()["current"]
        temp = current["temperature_2m"]
        wind = current["windspeed_10m"]
        weather_code = current["weathercode"]
        desc = WMO_CODES.get(weather_code, f"날씨 코드 {weather_code}")
        return f"{city} 현재 날씨: {desc}, 기온: {temp}°C, 풍속: {wind} km/h"
    except requests.exceptions.Timeout:
        return "날씨 정보를 가져오는 데 시간이 초과되었습니다. 잠시 후 다시 시도해주세요."
    except Exception as e:
        return f"날씨 정보를 가져오는 중 오류가 발생했습니다: {e}"
    
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Frankfurter api로 실시간 환율을 조회해 금액을 변환합니다.

    Args:
        amount: 변환할 금액
        from_currency: 기존 통화 코드(예: USD, EUR, KRW)
        to_currency: 변환 대상 통화 코드(예: USD, EUR, KRW)

    Returns:
        변환된 결과 문자열
    """
    
    from_c = from_currency.strip().upper()
    to_c = to_currency.strip().upper()
    
    if from_c == "KRW":
        return f"KRW는 Frankfurter API에서 지원되지 않습니다. 다른 통화를 사용해주세요."
    
    url = f"https://api.frankfurter.app/latest?from={from_c}&to={to_c}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        rate = data["rates"].get(to_c)
        if rate is None:
            return f"오류 {to_c} 통화를 찾을 수 없습니다."
        converted = amount * rate
        return f"{amount:.2f} {from_c} = {converted:.2f} {to_c} (환율: 1 {from_c} = {rate} {to_c})"
    except requests.exceptions.Timeout:
        return "환율 정보를 가져오는 데 시간이 초과되었습니다. 잠시 후 다시 시도해주세요."
    except Exception as e:
        return f"환율 정보를 가져오는 중 오류가 발생했습니다: {e}"
    
chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(
        tools=[get_current_weather, convert_currency],
        system_instruction=("당신은 날씨와 환율 정보를 제공하는 에이전트입니다. "
                            "반드시 도구를 사용해 최신 데이터를 조회하세요"
                            "도구에 에러가 발생하면 사용자에게 원일을 설명하세요"
        )
    ),
)

questions = [
    "서울이랑 도쿄 날씨 비교해줘",
    "100달러 한국돈으로 바꾸면 얼마야?",
    "파리 날씨 어때? 그리고 500유로를 달러로 환산해줘",
    "런던 날씨와 1000엔을 원화로 환산하는 것 둘 다 알려줘",
]

print("=" * 60)
for q in questions:
    print(f"[질문] {q}")
    r = chat.send_message(q)
    print(f"[답변] {r.text}")
    print("-" * 60)
        