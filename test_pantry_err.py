import asyncio, os, base64
from utils.ai_client import AIClient
from schemas.models import PantryInventory
from agents.prompts import PANTRY_AGENT_PROMPT

async def main():
    client = AIClient()
    with open('temp_pantry.jpg', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    messages = [
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": PANTRY_AGENT_PROMPT}, 
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]
        }
    ]
    try:
        res = await client.generate_vision(messages, PantryInventory)
        print("SUCCESS:", res)
    except Exception as e:
        print("ERROR TYPE:", type(e))
        print("ERROR:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
