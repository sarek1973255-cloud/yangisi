import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

# ----------------------------
# 1. orginfo.uz (example structure)
# ----------------------------
def scrape_orginfo(oked):
    url = f"https://orginfo.uz/search?q={oked}"

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for item in soup.find_all("div"):
        a = item.find("a")
        if a and a.get("href"):
            name = a.get_text(strip=True)
            link = a["href"]

            if name and "http" in link:
                results.append([name, link])

    return results


# ----------------------------
# 2. yellowpages (generic)
# ----------------------------
def scrape_yellowpages(oked):
    url = f"https://www.yellowpages.uz/search/{oked}"

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for a in soup.find_all("a"):
        href = a.get("href")
        name = a.get_text(strip=True)

        if href and name and len(name) > 3:
            if "http" in href:
                results.append([name, href])

    return results


# ----------------------------
# 3. goldenpages (generic)
# ----------------------------
def scrape_goldenpages(oked):
    url = f"https://goldenpages.uz/search/?q={oked}"

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for a in soup.find_all("a"):
        href = a.get("href")
        name = a.get_text(strip=True)

        if href and name and len(name) > 3:
            if "http" in href:
                results.append([name, href])

    return results


# ----------------------------
# CLEAN + MERGE + REMOVE DUPLICATES
# ----------------------------
def search_all(oked):
    all_results = []

    all_results += scrape_orginfo(oked)
    all_results += scrape_yellowpages(oked)
    all_results += scrape_goldenpages(oked)

    # duplicate remove
    seen = set()
    clean = []

    for name, link in all_results:
        key = link.lower()

        if key not in seen:
            seen.add(key)
            clean.append([name, link])

    return clean
