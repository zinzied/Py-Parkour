```text
  _____       _--_          _                   
 |  __ \     |  _ \        | |                  
 | |__) |   _| |_) |__ _ __| | ___ ___  _   _ _ __ 
 |  ___/ | | |  _ // _` | '__| |/ / _ \| | | | '__|
 | |   | |_| | | \ \ (_| | |  |   < (_) | |_| | |  
 |_|    \__, |_|  \_\__,_|_|  |_|\_\___/ \__,_|_|  
         __/ |                                     
        |___/                                      
```

> **Version**: 1.0.0  
> **Author**: zinzied (zinzied@gmail.com)

# 🏃 Py-Parkour: The Full-Stack Scraper Framework

**Py-Parkour** is a lightweight automation utility designed to solve the three biggest annoyances in modern web scraping:
1.  **Cookie Consents**: Detecting and destroying GDPR/modal popups.
2.  **Pagination**: Auto-detecting "Next" buttons or infinite scroll.
3.  **Verification Gates**: Generating temporary identities (Email/SMS) for signups.

It turns your scraper into a **workflow automation platform**.

---

## 📦 Installation

You can install the library directly:

```bash
pip install -e .[full]
```

Or using the standard requirements:

```bash
pip install -r requirements.txt
playwright install
```

---

## 🚀 How to Use It

### 1. The "Unified" Bot
The `ParkourBot` is your main entry point. It wraps a Playwright browser and gives you access to all gadgets.

```python
import asyncio
from py_parkour import ParkourBot

async def main():
    # Start the bot (headless=False to see it in action)
    bot = ParkourBot(headless=False)
    await bot.start()

    # Go to your target
    await bot.goto("https://target-website.com")

    # ... use gadgets here ...

    await bot.close()
```

### 2. 🍪 Gadget: Crusher (Cookie Bypasser)
Don't write brittle selectors for every "Accept Cookies" button. Let `Desctructor` handle it.

```python
# Automatically finds "Accept", "Agree", or high-z-index overlays and clicks them
await bot.crush_cookies()
```

### 3. 🧭 Gadget: Compass (Auto-Pagination)
Stop guessing if the site uses `?page=2` or a "Next >" button.

```python
# The bot will yield control for each page it finds
# It auto-detects "Next" buttons (by text/icon) or infinite scroll!
async for page_number in bot.crawl(max_pages=10):
    print(f"Scraping Page {page_number}: {bot.current_url}")
    # Extract your data here using standard Playwright methods
    # content = await bot.driver.page.content()
```

### 4. 🎭 Gadget: Disguises (Temp Identity)
Need to sign up to view data? Generate a burner identity.

```python
# 1. Get a fresh email
identity = await bot.identity.generate_identity(country="US")
print(f"Using email: {identity.email}")

# 2. Fill it into a form (example)
await bot.driver.page.fill("#email-input", identity.email)

# 3. Wait for the verification code (Magic!)
# This polls the temp-mail inbox for you
code = await bot.identity.wait_for_code()
await bot.driver.page.fill("#otp-input", code)
```

### 5. ✨ The "Magic" Auto-Setup
Try to automate the entire signup flow (Experimental).

```python
await bot.auto_setup_identity("https://example.com/signup")
```

---

## 🎯 Where to use it?

Py-Parkour is best for:

1.  **Complex Scraping**: Sites that require login or have heavy popups (e.g., News sites, E-commerce, heavily gated content).
2.  **QA Automation**: Testing "User Registration" flows without using real email addresses.
3.  **Bot Development**: Quickly spinning up bots that need to pass "verify your email" checks.

## 🏗 Architecture
- **Core**: Async Playwright wrapper.
- **Gadgets**: Modular tools attached to the bot (`.crusher`, `.compass`, `.identity`).

---

*Built with ❤️ for Scrapers who hate boilerplate.*
