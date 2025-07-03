import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the Excel input
input_file = "Input.xlsx"
df = pd.read_excel(input_file)

# Create directory for articles
os.makedirs("articles", exist_ok=True)

def extract_article_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Heuristically extract title and body text
        title = soup.find('h1')
        paragraphs = soup.find_all('p')

        title_text = title.get_text(strip=True) if title else ""
        body_text = " ".join(p.get_text(strip=True) for p in paragraphs)

        return title_text + "\n\n" + body_text
    except Exception as e:
        print(f"Failed to extract {url}: {e}")
        return ""

# Loop through each URL and extract article
for index, row in df.iterrows():
    url_id = str(row['URL_ID'])
    url = row['URL']
    
    text = extract_article_text(url)
    with open(f"articles/{url_id}.txt", "w", encoding="utf-8") as f:
        f.write(text)

print("✅ Article extraction complete!")
