# 🤖 Anti-Bot Strategy Guide

**Py-Parkour** uses a **"Prevention over Cure"** strategy. Instead of trying to break sophisticated Captchas (which is hard/expensive), it tries to avoid triggering them in the first place by acting human.

## 1. 🛡️ Prevention (Behavioral Evasion)
Cloudflare and Akamai analyze **how you move** and **how you type**.

| Feature | What it does | Why it helps |
| :--- | :--- | :--- |
| **GhostCursor** (`.ghost`) | Moves mouse in curves with acceleration/jitter. | Prevents "Teleportation" detection (checking `mouseEvent` coordinates). |
| **ChaosTyper** (`.typer`) | Types with random latency and typos. | Prevents "Machine Typing" detection (perfect 10ms intervals). |
| **Shadow** (`.shadow`) | Uses real Browser Headers & TLS Fingerprint. | Passes the "TCP/TLS Handshake" check that blocks Python `requests`. |

## 2. 🧩 Solving (If you get blocked)
If you *do* hit a Captcha (e.g. Turnstile, reCAPTCHA), **Py-Parkour** does not have a built-in solver yet, but its **Hybrid Architecture** allows you to solve it easily:

### Strategy A: Manual Assist (Hybrid)
1.  Run `bot = ParkourBot(headless=False)`.
2.  Wait for the user (you) to solve the Captcha manually in the window.
3.  Once solved, use `bot.shadow` to steal the "Clearance Cookie" and continue automatically.

### Strategy B: Plugin Integration
You can easily load existing solver plugins (like `2captcha-solver` or `nopecha`) into the browser context because `bot.driver` exposes the standard Playwright context.

```python
# Pseudo-code for loading a solver extension
await bot.driver.context.add_init_script(path="path/to/solver_plugin.js")
```
