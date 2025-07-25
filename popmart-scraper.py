import asyncio
import json
import os
from playwright.async_api import async_playwright
import sys

TARGET_KEYWORDS = ["THE MONSTERS", "Labubu"]
BASE_URL = "https://www.popmart.com"
OUTPUT_FILE = os.path.join("data", "products.json")

# Proxy config (replace with your credentials)
PROXY_SERVER = "http://us.decodo.com:10001"
PROXY_USERNAME = "username"
PROXY_PASSWORD = "password"

async def scrape_popmart():
    print("New arrivals scraping started...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                proxy={"server": PROXY_SERVER}
                )
            
            context = await browser.new_context(
                proxy={
                    "server": PROXY_SERVER,
                    "username": PROXY_USERNAME,
                    "password": PROXY_PASSWORD
                }
            )
            page = await context.new_page()
            await page.goto("https://www.popmart.com/us/new-arrivals", timeout=30000)
            await page.wait_for_selector("div.index_title__jgc2z")

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

            results = []

            sections = await page.query_selector_all("div.index_title__jgc2z")

            for section in sections:
                release_date = (await section.text_content()).strip()

                # Get sibling product list container
                sibling = await section.evaluate_handle("el => el.nextElementSibling")
                product_cards = await sibling.query_selector_all("div.index_productCardCalendarContainer__B96oH")

                for card in product_cards:
                    # Product title
                    title_elem = await card.query_selector("div.index_title__9DEwH span")
                    title = await title_elem.text_content() if title_elem else ""
                    if not any(keyword.lower() in title.lower() for keyword in TARGET_KEYWORDS):
                        continue

                    # Release time
                    time_elem = await card.query_selector("div.index_time__EyE6b")
                    time_text = await time_elem.text_content() if time_elem else "N/A"

                    # Product URL
                    a_elem = await card.query_selector("a[href^='/us']")
                    href = await a_elem.get_attribute("href") if a_elem else None
                    full_url = f"{BASE_URL}{href}" if href else "N/A"

                    # Build entry
                    result = {
                        "title": title.strip(),
                        "release_date": release_date.strip(),  # Raw text like "Upcoming JUL 11"
                        "release_time": time_text.strip(),     # Raw text like "09:00"
                        "url": full_url
                    }
                    results.append(result)

            await browser.close()

            # Save to JSON
            os.makedirs("data", exist_ok=True)
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"Scraped {len(results)} matching products. Saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error during scraping: {e}")
        sys.exit(1)  # Exit with error code 1 on failure


if __name__ == "__main__":
    asyncio.run(scrape_popmart())