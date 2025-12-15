# 🍳 Py-Parkour Cookbook: "How do I..."?

This reference maps common web actions to the specific **Py-Parkour** tools you should use.

## 1. 🔑 Login & Authentication
**Goal**: Sign into a website securely.

*   **Standard Way**: Use the Driver directly.
    ```python
    await bot.goto("https://site.com/login")
    await bot.driver.page.fill("#email", "user@example.com")
    await bot.driver.page.click("#login-btn")
    ```
*   **The "Human" Way (Anti-Bot Safe)**: Use **Ghost** and **Typer**.
    ```python
    # Move mouse naturally to the input
    await bot.ghost.click("#email")
    # Type with human speed and mistakes
    await bot.typer.type_human("#email", "user@example.com")
    ```

## 2. 📝 Inscription (Registration/Sign Up)
**Goal**: Create a new account, handling the "Verify your Email" step.

*   **Generate Identity**: Create a fake persona.
    ```python
    user = await bot.identity.generate_identity()
    print(f"Signing up as {user.email}")
    ```
*   **The "Magic" Auto-Setup**: Let the bot try to do it all (fill email -> wait -> submit code).
    ```python
    await bot.auto_setup_identity("https://site.com/signup")
    ```
*   **Manual Verification**:
    ```python
    # After you click "Send Code"...
    code = await bot.identity.wait_for_code()
    await bot.driver.page.fill("#otp-input", code)
    ```

## 3. 🔍 Search & Browsing
**Goal**: Find items and navigate through results.

*   **Search**:
    ```python
    await bot.typer.type_human("#search-bar", "Gaming Laptops")
    await bot.driver.page.keyboard.press("Enter")
    ```
*   **Pagination (The "Look" Phase)**: Use **Compass** to handle "Next" buttons or Infinite Scroll.
    ```python
    async for page_num in bot.compass.crawl(max_pages=5):
        print(f"Scraping page {page_num}...")
        # ... extract your data ...
    ```

## 4. 🕵️ Data Extraction ("Looking")
**Goal**: Get the data out.

*   **Standard HTML**:
    ```python
    titles = await bot.driver.page.locator(".product-title").all_text_contents()
    ```
*   **Hidden APIs (Advanced)**: Use **Radar** to catch the raw JSON.
    ```python
    # Just navigate, Radar watches in background
    latest_api_data = bot.radar.latest_json
    print(latest_api_data)
    ```
*   **Hard-to-Find Elements**: Use **Spatial** if IDs are messy.
    ```python
    # "Find the input right of the 'Price' label"
    input_el = await bot.spatial.find_right_of("label:has-text('Price')")
    ```

## 5. ⚡ Performance (Session Management)
**Goal**: Go faster after logging in.

*   **Session Stealing**: Use **Shadow** to move to a fast, headless client.
    ```python
    # 1. Log in with Browser...
    # 2. Steal session
    async with await bot.shadow.create_session() as session:
        # 3. Close browser to save RAM
        await bot.close()
        # 4. Continue fast
        resp = await session.get("https://site.com/api/private")
    ```

## 6. 🧹 Housekeeping
**Goal**: Cleaning up.

*   **Clear Cookies/Logout**:
    ```python
    await bot.driver.page.context.clear_cookies()
    ```
*   **Handle Popups**: Use **Crusher**.
    ```python
    await bot.crush_cookies()
    ```
