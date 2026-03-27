import snscrape.modules.twitter as sntwitter
import re

query = "wilbay.de"
max_tweets = 1000000

links = set()

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > max_tweets:
        break

    text = tweet.content

    found_links = re.findall(
        r'https?://(?:www\.)?wilbay\.de\S+',
        text
    )

    for link in found_links:
        links.add(link)

# simpan ke file
with open("wilbay_links.txt", "w", encoding="utf-8") as f:
    for link in links:
        f.write(link + "\n")

print(f"Total link: {len(links)}")