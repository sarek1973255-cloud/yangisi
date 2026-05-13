import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

UZB_HINTS = [
    ".uz", "uzbekistan", "tashkent", "toshkent",
    "samarkand", "andijan", "namangan", "bukhara",
    "mchj", "ooo", "oao"
]

BAD_WORDS = [
    "login", "sign", "account", "help", "support",
    "wiki", "wikipedia", "youtube", "facebook",
    "instagram", "maps", "translate", "news",
    "office", "microsoft", "google"
]


def get_yandex_results(query):
    url = f"https://yandex.com/search/?text={query}"

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for item in soup.select("li.serp-item"):
        a = item.select_one("a.organic__url-text")
        title = item.select_one("h2")

        if a and title:
            link = a.get("href")
            name = title.get_text(strip=True)
            results.append((name, link))

    return results


def is_valid(title, link):
    text = (title + " " + link).lower()

    for w in BAD_WORDS:
        if w in text:
            return True

    if "." not in link:
        return False

    return any(x in text for x in UZB_HINTS)


def search_by_oked(oked):
    query = f"{oked} kompaniya uzbekistan"
    raw = get_yandex_results(query)

    clean = []

    for title, link in raw:
        if is_valid(title, link):
            clean.append([title, link])

    return clean
