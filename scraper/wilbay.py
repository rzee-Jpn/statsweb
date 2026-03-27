import re
import time
import requests

# =========================
# CONFIG
# =========================
QUERY = "wilbay.de"
MAX_TWEETS = 300
OUTPUT_FILE = "wilbay_links.txt"

# regex target
REGEX = r'https?://(?:www\.)?wilbay\.de\S+'

# =========================
# SOURCE 1: SNSCRAPE
# =========================
def scrape_snscrape():
    print("[+] Try snscrape...")
    links = set()
    try:
        import snscrape.modules.twitter as sntwitter

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(QUERY).get_items()):
            if i > MAX_TWEETS:
                break

            found = re.findall(REGEX, tweet.content)
            links.update(found)

            time.sleep(0.5)  # anti-block ringan

        print(f"[snscrape] found: {len(links)}")
        return links

    except Exception as e:
        print("[snscrape] failed:", e)
        return set()


# =========================
# SOURCE 2: NITTER
# =========================
def scrape_nitter():
    print("[+] Try Nitter...")
    links = set()

    try:
        url = f"https://nitter.net/search?f=tweets&q={QUERY}"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)
        html = res.text

        found = re.findall(REGEX, html)
        links.update(found)

        print(f"[nitter] found: {len(links)}")
        return links

    except Exception as e:
        print("[nitter] failed:", e)
        return set()


# =========================
# MAIN FLOW
# =========================
def main():
    all_links = set()

    # coba snscrape dulu
    links1 = scrape_snscrape()
    all_links.update(links1)

    # fallback kalau kosong / sedikit
    if len(all_links) < 10:
        links2 = scrape_nitter()
        all_links.update(links2)

    # simpan hasil
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in sorted(all_links):
            f.write(link + "\n")

    print(f"[DONE] total links: {len(all_links)}")


if __name__ == "__main__":
    main()