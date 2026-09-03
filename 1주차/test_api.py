import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),'..', '.env'))

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY is not set in the environment variables.")
    print("위치를 확인하세요")
    exit(1)
    
print(f"API키 로드 성공 (앞 10자리: {api_key[:10]}...)")

client = genai.Client(api_key=api_key)  

print("\nGemini API 호출중")
response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = "인공지능 에이전트와 일반 챗봇의 차이점을 두문장으로 설명해줘",
    config=types.GenerateContentConfig(
        system_instruction="당신은 친절한 AI 에이전트입니다. 반드시 한국어로 대답합니다.",
    )
)

print("\nGemini API 응답")
print(" - " * 50)
print(response.text)
print(" - " * 50)
print(f"\n사용토큰: 입력 {response.usage_metadata.prompt_token_count}개, 출력 {response.usage_metadata.candidates_token_count}개")