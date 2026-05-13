import requests
from bs4 import BeautifulSoup

def search_companies(oked_code):
    try:
        url = "https://orginfo.uz/search?q=" + str(oked_code)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return ["Server error: " + str(response.status_code)]

        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        # 🔥 universal text olish (classga bog‘liq emas)
        for tag in soup.find_all(["a", "div", "span"]):
            text = tag.get_text(strip=True)

            if text:
                if len(text) > 5:
                    # garbage filter
                    if "OKED" not in text and "search" not in text.lower():
                        results.append(text)

        # duplicate remove
        seen = []
        for r in results:
            if r not in seen:
                seen.append(r)

        if not seen:
            return ["Hech narsa topilmadi"]

        return seen[:15]

    except Exception as e:
        return ["ERROR: " + str(e)]