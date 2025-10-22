import asyncio
import pandas as pd
from playwright.async_api import async_playwright
import os

OUTPUT_CSV = r"C:\Users\Sai Abhijeet\Desktop\Python Parsing\TV_flipkart\TV_Flipkart.csv"
START_URL = "https://www.flipkart.com/search?q=television&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"

async def safe_text(parent, selector):
    try:
        el = await parent.query_selector(selector)
        return (await el.text_content()).strip() if el else None
    except:
        return None

async def extract_product_data(page):
    await page.wait_for_timeout(2000)

    try:
        await page.wait_for_selector("div.KzDlHZ", timeout=10000)
    except:
        print("⚠️ No products found on this page.")
        return []

    product_cards = await page.query_selector_all("div._1AtVbE")

    extracted_data = []
    for card in product_cards:
        name = await safe_text(card, "div.KzDlHZ")
        price = await safe_text(card, "div.Nx9bqj._4b5DiR")
        rating = await safe_text(card, "div.XQDdHH")
        description = await safe_text(card, "div._6NESgJ")

        if name:
            extracted_data.append({
                "Product Name": name,
                "Price": price,
                "Rating": rating,
                "Description": description,
            })
    return extracted_data

async def paginate_all_data(start_url):
    all_products = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(start_url)

        # Close login popup if it appears
        try:
            close_btn = await page.wait_for_selector("button._2KpZ6l._2doB4z", timeout=5000)
            await close_btn.click()
        except:
            pass  # Popup not present

        page_num = 1
        while True:
            print(f"\n🔎 Scraping page {page_num}...")
            products = await extract_product_data(page)
            if not products:
                print("⚠️ No more products or page error.")
                break

            all_products.extend(products)

            try:
                next_btn = await page.query_selector("a._1LKTO3[rel='next']")
                if next_btn:
                    await next_btn.click()
                    await page.wait_for_timeout(2000)
                    page_num += 1
                else:
                    break
            except:
                print("❌ Pagination failed.")
                break

        await browser.close()
    return all_products

def save_to_csv(data, filepath):
    if not data:
        print("❌ No data to save.")
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"\n✅ CSV saved to: {filepath}")
    print(f"📊 Rows: {df.shape[0]}, Columns: {df.shape[1]}")

def main():
    data = asyncio.run(paginate_all_data(START_URL))
    save_to_csv(data, OUTPUT_CSV)

if __name__ == "__main__":
    main()
