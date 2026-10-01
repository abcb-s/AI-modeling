import sys
import math
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("계산/변환 도구 서버")

@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    """사칙연산을 수행합니다.

    Args:
        operation: 연산 종류. add / subtract / multiply / divide
        a: 첫 번째 숫자
        b: 두 번째 숫자
    """
    ops = {
        "add":      f"{a} + {b} = {a + b}",
        "subtract": f"{a} - {b} = {a - b}",
        "multiply": f"{a} x {b} = {a * b}",
        "divide":   f"{a} / {b} = {a / b:.6f}" if b != 0 else "오류: 0으로 나눌 수 없습니다.",
    }
    return ops.get(operation, f"지원하지 않는 연산: {operation}")

@mcp.tool()
def convert_temperature(celsius: float) -> str:
    """섭씨 온도를 화씨와 켈빈으로 변환합니다.

    Args:
        celsius: 변환할 섭씨 온도
    """
    return f"{celsius}C = {celsius * 9/5 + 32:.2f}F = {celsius + 273.15:.2f}K"

@mcp.tool()
def get_current_datetime() -> str:
    """현재 날짜와 시간을 반환합니다."""
    now = datetime.now()
    weekdays = ["월","화","수","목","금","토","일"]
    return now.strftime(f"%Y년 %m월 %d일 ({weekdays[now.weekday()]}요일) %H:%M:%S")

@mcp.tool()
def is_prime(n: int) -> str:
    """주어진 정수가 소수인지 판별합니다.

    Args:
        n: 확인할 양의 정수
    """
    if n < 2:
        return f"{n}은(는) 소수가 아닙니다."
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return f"{n}은(는) 소수가 아닙니다. ({i}의 배수)"
    return f"{n}은(는) 소수입니다."

if __name__ == "__main__":
    print("MCP 도구 서버 시작...", file=sys.stderr)
    mcp.run()
