import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Scraping the first 5 pages of quotes
base_url = "https://quotes.toscrape.com"
tags_to_keep = ["love", "inspirational", "life", "humor"]
quotes = []

for page in range(1, 6):
    response = requests.get(f"{base_url}/page/{page}/")
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_divs = soup.find_all("div", class_="quote")
    for quote_div in quote_divs:
        text = quote_div.find("span", class_="text").get_text()
        tags = [tag.get_text() for tag in quote_div.find_all("a", class_="tag")]
        if any(tag in tags_to_keep for tag in tags):
            quotes.append({"text": text, "tags": tags})

# Step 2: Logging in and getting the token
login_url = f"{base_url}/login"
login_data = {"username": "test", "password": "test"}
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
login_data["csrf_token"] = csrf_token
response = session.post(login_url, data=login_data)

# Extract the token from the session cookies
token = session.cookies.get("session")

# Step 3: Adding the first 2 pages of quotes with the tag "books"
for page in range(1, 3):
    response = session.get(f"{base_url}/tag/books/page/{page}/")
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_divs = soup.find_all("div", class_="quote")
    for quote_div in quote_divs:
        text = quote_div.find("span", class_="text").get_text()
        tags = [tag.get_text() for tag in quote_div.find_all("a", class_="tag")]
        quotes.append({"text": text, "tags": tags})

# Step 4: Removing duplicates
quotes_df = pd.DataFrame(quotes).drop_duplicates(subset=["text"])

# Step 5: Writing results to CSV
quotes_df.to_csv("results.csv", index=False)

# Adding the token to the CSV
with open("results.csv", "a") as file:
    file.write(f"\nToken: {token}")