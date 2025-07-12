import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from langgraph_server.agents import RemoteAgent

agent = RemoteAgent("http://localhost:8000/simple_agent")

"""

response = agent.invoke("Hola")
"""

"""
async def main():
    response = await agent.ainvoke("Hola")
    return response

print(asyncio.run(main()))
"""

"""
for chunk in agent.stream("hola"):
    print("CHUNK:", chunk)
"""


async def main():
    async for chunk in agent.astream("hola"):
        print("CHUNK:", chunk)


asyncio.run(main())
