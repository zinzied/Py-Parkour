import asyncio
from py_parkour import ParkourBot

async def main():
    bot = ParkourBot(headless=True)
    
    try:
        print("--- Starting Live Demo ---")
        await bot.start()
        
        # --- Scenario 1: Pagination on Hacker News ---
        try:
            print("\n# Scenario 1: Auto-Walking Hacker News (Pagination)")
            await bot.goto("https://news.ycombinator.com/")
            print(f"Landed on: {bot.current_url}")
            
            page_count = 0
            async for _ in bot.crawl(max_pages=2):
                page_count += 1
                try:
                    await bot.driver.page.wait_for_selector(".athing", timeout=5000)
                    title = await bot.driver.page.locator(".titleline >> a").first.text_content()
                    print(f"  [Page {page_count}] Top Story: {title[:50]}...")
                except Exception as scrape_err:
                    print(f"  [Page {page_count}] Scrape warning: {scrape_err}")
        except Exception as e:
            print(f"Scenario 1 Failed: {e}")

        # --- Scenario 2: Cookie Crushing on The Guardian ---
        try:
            print("\n# Scenario 2: Cookie Crushing (The Guardian)")
            await bot.goto("https://www.theguardian.com/international")
            print(f"Landed on: {bot.current_url}")
            
            # Wait for banner
            await asyncio.sleep(4)
            
            print("  Attempting to crush cookies...")
            await bot.crush_cookies()
            print("  Cookie crush command executed.")
            
            await asyncio.sleep(2) # Wait to see if it clicked
            
        except Exception as e:
            print(f"Scenario 2 Failed: {e}")

    except Exception as e:
        print(f"Live Demo Fatal Error: {e}")
    finally:
        await bot.close()
        print("\n--- Demo Finished ---")

if __name__ == "__main__":
    asyncio.run(main())
