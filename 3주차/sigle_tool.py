import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def calculate(operation: str, a: float, b: float) -> float:
    """사칙연산을 수행합니다.
    
    Args:
        operation:연산종류. "add(덧셈)", "subtract(뺄셈)", "multiply(곱셈)", "divide(나눗셈)" 중 하나
        
        a: 첫 번째 숫자
        b: 두 번째 숫자
        
    Returns:
        계산식과 결과를 담은  문자열
    """
    
    if operation == "add":
        result = a + b
        return f"{a} + {b} = {result}"
    elif operation == "subtract":
        result = a - b
        return f"{a} - {b} = {result}"
    elif operation == "multiply":
        result = a * b
        return f"{a} * {b} = {result}"
    elif operation == "divide":
        if b == 0:
            return "0으로는 나눌수 없습니다. "
        result = a / b
        return f"{a} / {b} = {result:.6f}"
    else:
        return f"지원하지 않는 연산: {operation}"
    
    chat = client.chat.create(
        model="gemini-3.1-flash-lite",
        config=types.GenerateContentConfig(
            tools=[calculate],
            system_instruction="당신은 수학계산을 도와주는 에이전트입니다."
                                "계산이 필요하면 무조건 calculate 도구를 사용하세요.",
        ),
    )
    
    questions = [
        "1234더하기5678은 얼마야?",
        "7나누기 3을 계산해줘",
        "99더하기 1은 맞아?",
        "1000빼기 337은?"
    ]
    
    print("=" * 55)
    for q in questions:
        print(f"질문: {q}")
        response = chat.send_message(q)
        print(f"답변: {response.text}")
        print("=" * 55)