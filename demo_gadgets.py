import asyncio
from py_parkour import ParkourBot

async def main():
    print("🧪 Starting New Gadgets Demo...")
    # We use headful to SEE the mouse movements and typing
    bot = ParkourBot(headless=False) 
    await bot.start()

    try:
        # Use demoqa which has clear labels
        url = "https://demoqa.com/text-box"
        print(f"Navigating to {url}...")
        await bot.goto(url)
        # await asyncio.sleep(1)

        # ---------------------------------------------------------
        # 1. 📐 Test Spatial Compass (Geometry Finding)
        # ---------------------------------------------------------
        print("\n[1] Testing Spatial Compass...")
        
        # Scenario: Find the input field that is visually to the RIGHT of the "Full Name" label
        target_label_sel = "#userName-label"
        
        print(f"    Looking for input RIGHT OF '#userName-label'...")
        # Try right_of first (desktop layout)
        username_input = await bot.spatial.find_right_of(target_label_sel, target_tag="input")
        
        if not username_input:
             print("    ⚠️ Not found to right, trying BELOW...")
             username_input = await bot.spatial.find_below(target_label_sel, target_tag="input")
        
        if username_input:
            print("    ✅ Spatial Compass found the input!")
            # Highlight it
            await username_input.evaluate("el => el.style.border = '4px solid red'")
        else:
            print("    ❌ Spatial Compass failed to find input.")
            return

        # ---------------------------------------------------------
        # 2. 🖱️ Test Ghost Cursor (Bezier Movement)
        # ---------------------------------------------------------
        print("\n[2] Testing Ghost Cursor...")
        print("    Moving mouse to the found input naturally...")
        
        box = await username_input.bounding_box()
        if box:
            center_x = box['x'] + box['width']/2
            center_y = box['y'] + box['height']/2
            
            await bot.ghost.move_to(x=center_x, y=center_y)
            print("    ✅ Mouse moved (check visual).")

        # ---------------------------------------------------------
        # 3. ⌨️ Test Chaos Typer (Human Typing)
        # ---------------------------------------------------------
        print("\n[3] Testing Chaos Typer...")
        print("    Typing 'John Doe' with mistakes...")
        
        # Click first (using standard click or ghost click to focus)
        await bot.ghost.click("#userName") 
        
        await bot.typer.type_human("#userName", "John Doe", mistake_chance=0.2)
        print("    ✅ Typing complete.")

        print("\n--- Demo Finished ---")
        await asyncio.sleep(2) # Let user see result

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
