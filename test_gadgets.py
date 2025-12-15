import asyncio
from py_parkour import ParkourBot
import sys

async def test_radar(bot):
    print("\n[TEST] 📡 Testing Radar...")
    print("  > Navigating to a JSON endpoint...")
    
    # Reset radar before test
    if bot.radar:
        bot.radar.clear()
        
    await bot.goto("https://jsonplaceholder.typicode.com/todos/1")
    
    # Wait for network idle to ensure response is captured
    await bot.driver.page.wait_for_load_state("networkidle")
    await asyncio.sleep(1) # Extra buffer
    
    latest = bot.radar.latest_json
    print(f"  > Captured Data: {str(latest)[:60]}...")
    
    if latest and latest.get('id') == 1:
        print("  > ✅ Radar PASS: Captured expected JSON data.")
        return True
    else:
        print(f"  > ❌ Radar FAIL: Expected 'id': 1, got {latest}")
        return False

async def test_compass(bot):
    print("\n[TEST] 🧭 Testing Compass...")
    print("  > Navigating to paginated site (books.toscrape.com)...")
    
    await bot.goto("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
    
    pages_visited = []
    max_pages = 2
    
    print(f"  > Attempting to crawl {max_pages} pages...")
    async for page_num in bot.crawl(max_pages=max_pages):
        url = bot.current_url
        print(f"    - Visited Page {page_num}: {url}")
        pages_visited.append(url)
        
    # Validation
    if len(pages_visited) >= 2:
        # Check if URLs are different
        if pages_visited[0] != pages_visited[1]:
            print("  > ✅ Compass PASS: Successfully navigated to multiple pages.")
            return True
        else:
            print("  > ❌ Compass FAIL: URL did not change between iterations.")
            return False
    else:
         print(f"  > ❌ Compass FAIL: Only visited {len(pages_visited)} pages, expected {max_pages}.")
         return False

async def main():
    print("🚀 Starting Gadget Tests (Radar & Compass)...")
    bot = ParkourBot(headless=True)
    
    try:
        await bot.start()
        
        # Run Tests
        radar_result = await test_radar(bot)
        compass_result = await test_compass(bot)
        
        print("\n" + "="*30)
        print("📊 TEST SUMMARY")
        print("="*30)
        print(f"📡 Radar:   {'PASSED ✅' if radar_result else 'FAILED ❌'}")
        print(f"🧭 Compass: {'PASSED ✅' if compass_result else 'FAILED ❌'}")
        print("="*30)
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
    finally:
        await bot.close()
        print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
