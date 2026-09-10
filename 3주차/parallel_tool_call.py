import datetime
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def get_weather(city: str) -> str:
    """도시의 날씨(mock)를 반환합니다 .
    
    Args:
        city: 날씨를 가져올 도시 이름(예: 서울, 부산, 대구)
        
    Returns:
        도시의 날씨 정보 문자열
    """

    data = {
        "서울": "맑음, 23C, 습도 55%",
        "부산": "흐림, 26C, 습도 70%",
        "대구": "맑음, 28C, 습도 40%",
        "인천": "구름, 21C, 습도 80%"
    }
    
    return data.get(city, f"{city}의 날씨 정보가 없습니다.")

def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """환율(mock)을 반환합니다.
    
    Args:
        from_currency: 기준 통화 코드(예: USD, EUR, KRW)
        to_currency: 변환 대상 통화 코드(예: USD, EUR, KRW)
        
    Returns:
        환율 정보 문자열
    """
    
    rates = {
        ("USD","KRW"): 1352.5,
        ("EUR","KRW"): 1468.3,
        ("JPY","KRW"): 9.12,
        ("USD","EUR"): 0.926,
        ("EUR","USD"): 1.08,
    }
    
    rate = rates.get((from_currency.upper(), to_currency.upper()))
    if rate:
        return f"1 {from_currency.upper()} = {rate} {to_currency.upper()}"
    return f"{from_currency.upper()}에서 {to_currency.upper()}로의 환율 정보가 없습니다."

def get_current_time(timezone: str) -> str:
    """현재 시각을 반환합니다.

    Args:
        timezone: 시간대 이름(예: KST, UTC, EST). 현재는 KST만 지원.

    Returns:
        현재 날짜와 시각 문자열
    """
    
    now = datetime.datetime.now()
    return f"{timezone.upper()} 현재 시각: {now.strftime('%Y-%m-%d %H:%M:%S')}"

chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(
        tools=[get_weather, get_exchange_rate, get_current_time],
        system_instruction="질문에 필요한 도구는 모두 사용하세요."
                            "여러 정보가 필요하면 동시에 조회를 해도 됩니다"
    ),
)

query = "서울의 날씨와 USD에서 KRW로의 환율, 현재 시각을 알려줘"
print(f"질문: {query}\n")
response = chat.send_message(query)
print(f"응답: {response.text}\n")

print("=" * 55)

query2="부산과 대구의 날씨를 비교해줘"
print(f"질문: {query2}\n")
response2 = chat.send_message(query2)
print(f"응답: {response2.text}\n")