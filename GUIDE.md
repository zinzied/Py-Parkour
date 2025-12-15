# 🧭 Py-Parkour Gadgets Guide

This guide focuses on two powerful gadgets in the `py-parkour` library: **Compass** and **Radar**. These tools help you navigate complex websites and discover hidden APIs.

## 1. 📡 Radar (.radar)
**The Passive API Detector**

### What is it?
The Radar gadget automatically listens to background network traffic while your bot navigates. It specifically looks for JSON responses, which often indicate an underlying API that powers the website.

### Why use it?
Modern websites (SPAs) often load data via APIs. Instead of parsing messy HTML with selectors, you can often just grab the clean JSON data that the Radar captured.

### Basic Usage
The Radar starts automatically when you run `await bot.start()`.

```python
import asyncio
from py_parkour import ParkourBot

async def example_radar():
    bot = ParkourBot(headless=True)
    await bot.start()

    print("Visiting a site...")
    # Navigate to a site that loads data dynamically
    await bot.goto("https://jsonplaceholder.typicode.com/posts/1")
    
    # Wait a moment for network requests to finish
    await asyncio.sleep(2)

    # Access the most recent JSON captured
    latest_data = bot.radar.latest_json
    if latest_data:
        print("🎉 Capture Success!")
        print(f"Data: {latest_data}")
    else:
        print("No JSON found.")

    await bot.close()
```

### Advanced: Inspecting All Requests
You can also inspect the history of all JSON requests captured during the session. This is useful for finding specific API endpoints (e.g., user lists, product catalogs).

```python
# After navigation...
for req in bot.radar.requests:
    print(f"URL: {req['url']}")
    print(f"Method: {req['method']}")
    print(f"Payload Preview: {req['payload_preview']}")
    print("---")
```

---

## 2. 🧭 Compass (.compass)
**The Auto-Navigator**

### What is it?
The Compass gadget handles pagination for you. It tries to automatically detect how to get to the next page, whether it's by clicking a "Next" button or scrolling down (infinite scroll).

### Strategies
The Compass uses two main strategies:
1.  **Keyword Matching**: Looks for buttons with text like "Next", "Older", ">", ">>", etc.
2.  **Infinite Scroll**: Checks if the page height increases after scrolling to the bottom.

### Basic Usage
The easiest way to use the Compass is through the `bot.crawl()` helper methods.

```python
import asyncio
from py_parkour import ParkourBot

async def example_compass():
    bot = ParkourBot(headless=False)
    await bot.start()
    await bot.goto("https://books.toscrape.com/")

    # Scroll through up to 5 pages
    # The loop yields control back to you for each page found
    async for page_num in bot.crawl(max_pages=5):
        current_url = bot.current_url
        print(f"📍 Scraping Page {page_num} at {current_url}")
        
        # ... Perform your scraping logic here (e.g. finding products) ...
        # items = await bot.driver.page.locator(".product_pod").all_text_contents()
        # print(f"Found {len(items)} items")

    await bot.close()
```

### Manual Control
You can also access the compass directly if you need more granular control, though `bot.crawl()` is recommended for most cases.

```python
# Inside your main loop
await bot.compass.crawl(max_pages=3) 
```

---

## 🔗 How they relate to the Library
Both `Radar` and `Compass` are **Gadgets** attached to the `ParkourBot`.

*   **Initialization**: They are initialized in `bot.start()` and attached to `bot.radar` and `bot.compass`.
*   **Integration**:
    *   **Radar** hooks into the Playwright page's `on("response")` event to passively collect data without interrupting your flow.
    *   **Compass** actively interacts with the page (clicking or scrolling) when you iterate through it using `bot.crawl()`.

They are designed to work together: you might use **Compass** to move to the next page, and **Radar** to collect the API data triggered by that navigation!
