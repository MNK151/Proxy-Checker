import requests
from bs4 import BeautifulSoup
import csv

with open(r"C:\Users\Sai Abhijeet\Desktop\Python Parsing\Proxy\valid_proxy.txt", "r") as f:
    proxies = f.read().split("\n")


sites_to_check = []
base_url = "https://www.flipkart.com/search?q=television&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_4_0_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_4_0_na_na_na&as-pos=4&as-type=HISTORY&suggestionId=television&requestId=1e5a845e-a8d9-4a94-ab0b-fb7445b58fc5&page={page}"
for i in range(1, 6):
    sites_to_check.append(base_url.format(page=i))


output_file = open(r"C:\Users\Sai Abhijeet\Desktop\Python Parsing\Proxy\tv_flipkart.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(output_file)
writer.writerow(["Name", "Price", "Image URL"])

counter = 0

for site in sites_to_check:
    try:
        proxy = proxies[counter % len(proxies)]
        print(f"\n🔎 Checking Page {counter + 1} using proxy: {proxy}")
        res = requests.get(site, proxies={"http": proxy, "https": proxy}, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        print(f"✅ Status Code: {res.status_code}")

        soup = BeautifulSoup(res.text, "html.parser")
        print("\n📦 Scraped Products:\n")
        products = soup.find_all("div", {"class": "_75nlfW"})

        for product in products:
            name_tag = product.find("div", class_="KzDlHZ")
            price_tag = product.find("div", class_="Nx9bqj _4b5DiR")
            image_tag = product.find("img", class_="DByuf4")

            if name_tag and price_tag and image_tag:
                name = name_tag.text.strip()
                price = price_tag.text.strip()
                image_url = image_tag.get("src")

                writer.writerow([name, price, image_url])  # ⬅️ Save to CSV

                print(f"Name: {name}")
                print(f"Price: {price}")
                print(f"Image URL: {image_url}")
                print("-" * 60)

    except Exception as e:
        print("❌ Failed:", e)
    finally:
        counter += 1

output_file.close()  # ✅ Close CSV
print("\n📁 Data saved to flipkart_products.csv")
