import asyncio
from py_parkour import ParkourBot

async def main():
    print("👻 Starting 'Clientless' Shadow Demo...")
    print("Objective: Start in Browser -> Steal Session -> Close Browser -> Continue Scraping")

    # 1. Start the Browser (The "Navigator")
    # We start headless, but it IS a browser session.
    bot = ParkourBot(headless=True)
    await bot.start()
    
    print("\n[Step 1] Browser: Navigating to set authentication cookies...")
    # We assume we log in here. For demo, we just set a cookie.
    await bot.goto("https://postman-echo.com/cookies/set?auth_token=SECRET_SESSION_ID_12345")
    await asyncio.sleep(1)
    print("   ✅ Browser: Cookies set.")

    # 2. Steal the Session (Shadow Gadget)
    print("\n[Step 2] Shadow: cloning session state...")
    # This creates a lightweight aiohttp ClientSession with the browser's cookies/UA
    clientless_session = await bot.shadow.create_session()
    print("   ✅ Shadow: Session cloned.")

    # 3. KILL THE BROWSER (Remove "Navigator")
    print("\n[Step 3] Browser: Terminating Navigator...")
    await bot.close()
    print("   ✅ Browser CLOSED. We are now purely clientless.")

    # 4. Continue Scraping (Clientless)
    print("\n[Step 4] Clientless: Fetching protected data...")
    try:
        # We use the 'clientless_session' object which is standard aiohttp
        async with clientless_session.get("https://postman-echo.com/cookies") as response:
            if response.status == 200:
                data = await response.json()
                cookies = data.get("cookies", {})
                
                print(f"   📡 Server Response: {data}")
                
                if cookies.get("auth_token") == "SECRET_SESSION_ID_12345":
                    print("   🎉 SUCCESS! We accessed the authenticated endpoint WITHOUT the browser.")
                else:
                    print("   ❌ FAILED. Session was lost.")
            else:
                print(f"   ❌ Error: {response.status}")
                
    finally:
        # Don't forget to close the aiohttp session
        await clientless_session.close()
    
    print("\n--- Demo Finished ---")

if __name__ == "__main__":
    asyncio.run(main())
