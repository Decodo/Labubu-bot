import sys
import asyncio
from playwright.async_api import async_playwright

# Proxy config (replace with your credentials)
PROXY_SERVER = "http://us.decodo.com:10001"
PROXY_USERNAME = "username"
PROXY_PASSWORD = "password"

async def run(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False, # Visible browser for purchase
                proxy={"server": PROXY_SERVER}
                ) 
            context = await browser.new_context( # Create a new incognito context
                proxy={
                    "server": PROXY_SERVER,
                    "username": PROXY_USERNAME,
                    "password": PROXY_PASSWORD
                }
            )  
            page = await browser.new_page()
            await page.goto(url)

            # Try to close location popup if present
            try:
                await page.wait_for_selector("div.index_siteCountry___tWaj", timeout=15000)
                popup_selector = "div.index_siteCountry___tWaj"
                # Wait briefly (2 seconds) for popup to appear without failing if it doesn't
                await page.wait_for_selector(popup_selector, timeout=2000)
                await page.click(popup_selector)
                print("Closed location pop-up.")
            except Exception:
                # Popup not present — continue normally
                print("No location pop-up detected.")

            # Close policy acceptance pop-up if present (after country pop-up)
            try:
                policy_selector = "div.policy_acceptBtn__ZNU71"

                # Wait until it's visible
                await page.wait_for_selector(policy_selector, timeout=8000, state="visible")

                # Get the element
                policy_btn = await page.query_selector(policy_selector)

                if policy_btn:
                    await asyncio.sleep(1)  # slight buffer for JS readiness
                    await policy_btn.click()
                    print("Clicked policy ACCEPT div.")
                else:
                    print("Could not find the policy ACCEPT div.")
            except Exception as e:
                print(f"Policy ACCEPT pop-up not detected or failed to click: {e}")

            
            # Wait for ADD TO BAG button and click it
            add_to_bag_selector = "div.index_usBtn__2KlEx.index_red__kx6Ql.index_btnFull__F7k90"
            
            # Wait and click button safely
            try:
                await page.wait_for_selector(add_to_bag_selector, timeout=15000)  # 15 seconds timeout
                await page.click(add_to_bag_selector)
                print("Clicked 'ADD TO BAG' button.")
            except Exception as e:
                print(f"Failed to find or click 'ADD TO BAG' button: {e}")
                await browser.close()
                return 1  # Return error code
            
            await asyncio.sleep(3)  # Give it time to process

            # Go to the shopping cart page
            try:
                await page.goto("https://www.popmart.com/us/largeShoppingCart")
                print("Navigated to shopping cart.")
                # Click the checkbox to select all items
                await page.click("div.index_checkbox__w_166")
                # Keep the browser open to allow manual checkout
                print("Browser will stay open for manual checkout. Close it when done.")
                #await asyncio.Future()  # Keeps script running indefinitely until manually closed
                await page.wait_for_event("close", timeout=0)  # Wait until user closes the visible browser tab
            except Exception as e:
                print(f"Failed during checkout preparation: {e}")
                return 1  # Return error code
            finally:
                await context.close() # Clean up incognito session
                await browser.close() # Fully shut down Playwright
            
            return 0  # Success
            
    except Exception as e:
        print(f"Fatal error in purchase bot: {e}")
        return 1  # Return error code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 purchase-bot.py <product_url>")
        sys.exit(1)
    
    product_url = sys.argv[1]
    exit_code = asyncio.run(run(product_url))
    sys.exit(exit_code)