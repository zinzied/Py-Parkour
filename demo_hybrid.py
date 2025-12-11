import asyncio
from py_parkour import ParkourBot

async def main():
    print("--- 🕵️‍♀️ Starting Hybrid Demo ---")
    bot = ParkourBot(headless=True)
    await bot.start()

    try:
        # TEST 1: RADAR
        print("\n[1] Testing Radar (API Detector)...")
        # We visit a site that fetches JSON
        await bot.goto("https://jsonplaceholder.typicode.com/posts/1")
        # Wait a bit for the response to be captured
        await asyncio.sleep(2)
        
        latest = bot.radar.latest_json
        if latest and latest.get('id') == 1:
            print(f"✅ Radar Success! Captured JSON: {str(latest)[:50]}...")
        else:
            print(f"❌ Radar Fail. Captured: {latest}")

        # TEST 2: SHADOW
        print("\n[2] Testing Shadow (Session Bridge)...")
        # Let's go to postman-echo to set a cookie
        await bot.goto("https://postman-echo.com/cookies/set?my_cookie=shadow_rules")
        await asyncio.sleep(1)
        
        # Create shadow session
        session = await bot.shadow.create_session()
        
        # Verify cookies in the new session
        async with session.get("https://postman-echo.com/cookies") as resp:
            if resp.status != 200:
                print(f"❌ API Error: {resp.status} - {await resp.text()}")
            else:
                data = await resp.json()
                cookies = data.get("cookies", {})
                if cookies.get("my_cookie") == "shadow_rules":
                     print(f"✅ Shadow Success! Transferred cookie: {cookies}")
                else:
                     print(f"❌ Shadow Fail. Cookies: {cookies}")
        
        await session.close()

    finally:
        await bot.close()
        print("\n--- Demo Finished ---")

if __name__ == "__main__":
    asyncio.run(main())
