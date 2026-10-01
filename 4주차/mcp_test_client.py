import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).parent / "mcp_tool_server.py"

async def main():
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("사용 가능한 도구:", [t.name for t in tools.tools])

            calls = [
                ("calculate", {"operation": "multiply", "a": 12, "b": 7}),
                ("convert_temperature", {"celsius": 36.5}),
                ("get_current_datetime", {}),
                ("is_prime", {"n": 97}),
            ]
            for name, args in calls:
                result = await session.call_tool(name, args)
                print(f"{name}({args}) -> {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
