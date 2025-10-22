import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# --- IMPORTANT: VERIFY AND CORRECT THIS PATH ---
CHROMEDRIVER_PATH = r"C:\Users\Sai Abhijeet\Desktop\Python Parsing\Selenium\chromedriver.exe"

# Setup Chrome Options
options = Options()
# options.add_argument("--headless")  # Keep this commented out for now so you can see the browser open and debug element finding
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

if not os.path.exists(CHROMEDRIVER_PATH):
    print(f"Error: chromedriver.exe not found at '{CHROMEDRIVER_PATH}'")
    print("Please ensure you have downloaded the correct ChromeDriver version (matching your Chrome browser, Version 137.x.x.x) and placed it at the specified path.")
    exit()

try:
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"Failed to start ChromeDriver. Error: {e}")
    print("Please ensure your ChromeDriver version matches your Chrome browser version precisely (Chrome 137.x.x.x needs ChromeDriver 137.x.x.x).")
    print("Visit https://googlechromelabs.github.io/chrome-for-testing/ to download the correct driver.")
    exit()

product_names = []
product_prices = []
desc = []
rating = []

for page in range(1, 20):
    print(f"\n🔎 Scraping page {page}...")
    url = f"https://www.flipkart.com/audio-video/pr?sid=0pm&page={page}"
    try:
        driver.get(url)
        time.sleep(4)

        # --- CRITICAL: INSPECT FLIPKART TO GET THE CORRECT PRODUCT CONTAINER CLASS ---
        # Right-click a product -> Inspect. Find the <div> that wraps a whole product listing.
        # It's often something like "_1AtPxX" or "_1YokD2" or "_1GRhLX"
        # You may need to experiment. Try the most encompassing div for one product.
        # Example attempts:
        # product_containers = driver.find_elements(By.CSS_SELECTOR, "div._1AtPxX")
        # product_containers = driver.find_elements(By.CSS_SELECTOR, "div._1YokD2 div._1AtPxX") # if there's a parent wrapper
        product_containers = driver.find_elements(By.CSS_SELECTOR, "div._1GRhLX") # A common product card class

        if not product_containers:
            print(f"No product containers found on page {page} with current selectors. Trying alternatives...")
            # Fallback to another common selector if the first one doesn't work
            product_containers = driver.find_elements(By.CSS_SELECTOR, "div._1AtPxX")
            if not product_containers:
                print(f"Still no product containers found on page {page}. Page might be empty or structure changed. Exiting.")
                break

        for container in product_containers:
            name = None
            price = None
            description = None
            product_rating = None

            try:
                # --- VERIFY THESE CLASS NAMES BY INSPECTING FLIPKART'S HTML ---
                name_element = container.find_element(By.CLASS_NAME, "wjcEIp")
                name = name_element.text.strip()
            except NoSuchElementException:
                pass

            try:
                price_element = container.find_element(By.CLASS_NAME, "Nx9bqj")
                price = price_element.text.strip()
            except NoSuchElementException:
                pass

            try:
                desc_element = container.find_element(By.CLASS_NAME, "NqpwHC")
                description = desc_element.text.strip()
            except NoSuchElementException:
                pass

            try:
                rating_element = container.find_element(By.CLASS_NAME, "XQDdHH")
                product_rating = rating_element.text.strip()
            except NoSuchElementException:
                pass

            product_names.append(name)
            product_prices.append(price)
            desc.append(description)
            rating.append(product_rating)

    except Exception as e:
        print(f"An unexpected error occurred on page {page}: {e}")
        continue # Continue to the next page even if one fails

driver.quit()

df = pd.DataFrame({
    "Product Name": product_names,
    "Prices": product_prices,
    "Descriptions": desc,
    "Rating": rating
})

output_csv_path = r"C:\Users\Sai Abhijeet\Desktop\Python Parsing\Audio_flipkart\audio_flipkart.csv"
df.to_csv(output_csv_path, index=False)
print(f"✅ Full data saved to {output_csv_path}")