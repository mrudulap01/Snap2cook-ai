import asyncio
from agents.pantry_agent import PantryInventoryAgent
async def main():
    agent = PantryInventoryAgent()
    print(await agent.process('temp_pantry.jpg'))
asyncio.run(main())
