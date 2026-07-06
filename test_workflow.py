import asyncio
from agents.orchestrator import Snap2CookOrchestrator

async def main():
    orchestrator = Snap2CookOrchestrator()
    try:
        result = await orchestrator.run_full_workflow("temp_dish.jpg")
        print("SUCCESS")
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(main())
