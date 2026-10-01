"""SSE 트랜스포트 MCP 서버 - HTTP로 여러 클라이언트가 접속 가능"""
import datetime
from mcp.server.fastmcp import FastMCP

# --- SSE 서버 설정 ---
mcp = FastMCP(
    "sse-demo",
    host="0.0.0.0",   # 모든 네트워크 인터페이스에서 수신
    port=8080,         # HTTP 포트
)


@mcp.tool()
def server_time() -> str:
    """서버의 현재 시각을 반환합니다."""
    return f"서버 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


@mcp.tool()
def echo(message: str) -> str:
    """메시지를 그대로 돌려보냅니다. 연결 테스트용.

    Args:
        message: 에코할 텍스트
    Returns:
        동일한 메시지 (서버 경유 확인용 prefix 포함)
    """
    return f"[SSE 서버 에코] {message}"


@mcp.tool()
def fibonacci(n: int) -> str:
    """n번째 피보나치 수를 계산합니다.

    Args:
        n: 피보나치 수열의 인덱스 (1 이상 50 이하)
    Returns:
        n번째 피보나치 수
    """
    if not 1 <= n <= 50:
        return "오류: n은 1 이상 50 이하여야 합니다."
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return f"피보나치({n}) = {b}"


if __name__ == "__main__":
    print("SSE MCP 서버 시작: http://localhost:8080")
    print("Inspector: npx @modelcontextprotocol/inspector --server-url http://localhost:8080/sse")
    mcp.run(transport="sse")
