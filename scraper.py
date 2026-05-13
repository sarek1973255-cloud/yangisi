import requests
from bs4 import BeautifulSoup

BASE_URL = "https://orginfo.uz/search?q="

def search_companies(oked_code):
    url = BASE_URL + oked_code
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    # ⚠️ selectorlar taxminiy, saytdan inspect qilish kerak
    cards = soup.find_all("div", class_="company-card")

    for c in cards[:10]:
        name = c.find("a").text.strip() if c.find("a") else "No name"
        phone = c.find("span", class_="phone")
        phone = phone.text.strip() if phone else "No phone"

        results.append(f"{name} | {phone}")

    return results
