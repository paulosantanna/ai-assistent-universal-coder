import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "medical_research_mcp.server"],
    )

    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            response = await session.list_tools()

            print(f"MCP conectado. Ferramentas encontradas: {len(response.tools)}")
            for tool in response.tools:
                print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())
