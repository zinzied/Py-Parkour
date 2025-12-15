import asyncio
from py_parkour import ParkourBot
from py_parkour.gadgets.solicitor import CaptchaSolver, TwoCaptchaSolver, Solicitor

# Define a Mock Solver for internal testing without paying for API calls
class MockSolver(CaptchaSolver):
    async def solve(self, captcha_type: str, url: str, site_key: str, **kwargs) -> str:
        print(f"   [MockSolver] Request: Type={captcha_type}, Key={site_key}, Extra={kwargs}")
        await asyncio.sleep(1) # Simulate network delay
        print("   [MockSolver] Solved!")
        return f"MOCK_{captcha_type.upper()}_TOKEN_123"

async def main():
    print("🧪 Testing Solicitor Gadget (Mock Mode)...")
    
    bot = ParkourBot(headless=True)
    await bot.start()

    try:
        # 1. Setup Mock
        mock_solver = MockSolver()
        bot.solicitor.set_solver(mock_solver)
        print("✅ Solver Set.")

        # --- Test 1: ReCaptcha V2 (Injection) ---
        print("\n[Test 1] ReCaptcha V2...")
        # Inject fake element
        await bot.driver.page.evaluate('''
            const div = document.createElement('div');
            div.setAttribute('data-sitekey', '6LeIpcuUAAAAAN-PJC1aOGNOpo7kQA');
            document.body.appendChild(div);
            
            const txt = document.createElement('textarea');
            txt.id = 'g-recaptcha-response';
            document.body.appendChild(txt);
        ''')

        await bot.solicitor.solve_recaptcha_v2()
        
        token = await bot.driver.page.evaluate('document.getElementById("g-recaptcha-response").innerHTML')
        if "MOCK_RECAPTCHA_V2_TOKEN" in token:
            print(f"✅ PASS: V2 Token injected: {token}")
        else:
            print(f"❌ FAIL: V2 Token mismatch: {token}")

        # --- Test 2: Turnstile (Injection) ---
        print("\n[Test 2] Cloudflare Turnstile...")
        # Inject fake turnstile element
        await bot.driver.page.evaluate('''
            const t_div = document.createElement('div');
            t_div.className = 'cf-turnstile';
            t_div.setAttribute('data-sitekey', '0x4AAAAAAAC3A-');
            document.body.appendChild(t_div);

            const t_input = document.createElement('input');
            t_input.name = 'cf-turnstile-response';
            document.body.appendChild(t_input);
        ''')
        
        await bot.solicitor.solve_turnstile()

        t_token = await bot.driver.page.evaluate('document.getElementsByName("cf-turnstile-response")[0].value')
        if "MOCK_TURNSTILE_TOKEN" in t_token:
             print(f"✅ PASS: Turnstile Token injected: {t_token}")
        else:
             print(f"❌ FAIL: Turnstile Token mismatch: {t_token}")
             
        # --- Test 3: ReCaptcha V3 (Return only) ---
        print("\n[Test 3] ReCaptcha V3...")
        v3_token = await bot.solicitor.solve_recaptcha_v3("SITE_KEY_V3", action="login", min_score=0.7)
        print(f"✅ PASS: V3 Token retrieved: {v3_token}")


    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
