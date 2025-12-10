import asyncio
from py_parkour import ParkourBot

async def main():
    print("Initializing ParkourBot...")
    bot = ParkourBot(headless=True)
    
    try:
        print("Starting Bot...")
        await bot.start()
        
        # Test 1: Navigation
        print("Testing Navigation to example.com...")
        await bot.goto("https://example.com")
        print(f"Current URL: {bot.current_url}")
        
        # Test 2: Identity Generation
        print("Testing Identity Generation...")
        identity = await bot.identity.generate_identity()
        print(f"Generated Identity: {identity.email}")
        
        # Test 3: Cookie Crusher (Mock check, example.com has no cookies usually)
        print("Testing Cookie Crusher...")
        await bot.crush_cookies() # Should just print "No obvious cookie banner found" or similar
        
        # Test 4: Compass (Pagination)
        print("Testing Compass (Pagination)...")
        # Example.com has no pagination, so it should loop once and stop.
        count = 0
        async for _ in bot.crawl(max_pages=2):
            count += 1
            print(f"Scraping page {count}")
        print("Pagination finished.")

    except Exception as e:
        print(f"Verification Failed: {e}")
    finally:
        await bot.close()
        print("Bot Closed.")

if __name__ == "__main__":
    asyncio.run(main())
