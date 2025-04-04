from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time

# List of keywords to search for TED Talks
keywords = [
    "motivation TED talk",
    "self-help TED talk",
    "depression TED talk",
    "stress TED talk",
    "happiness TED talk",
    "mental health TED talk",
    "productivity TED talk",
    "mindfulness TED talk",
    "resilience TED talk",
    "personal growth TED talk",
    "confidence TED talk",
    "leadership TED talk",
    "success TED talk",
    "inspiration TED talk",
    "focus TED talk",
    "ambition TED talk",
    "hard work TED talk",
    "ethics TED talk",
    "positive thinking TED talk",
    "Islam TED talk",
    "Muslim TED talk",
    "Quran TED talk",
    "Islamic culture TED talk",
    "Islamic history TED talk",
    "faith TED talk",
    "spirituality TED talk"
]

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver_path = "chromedriver-linux64/chromedriver"  
# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(options=chrome_options)

# File to save the links
csv_file = "ted_talk_youtube_links.csv"

if os.path.exists(csv_file):

    df_existing = pd.read_csv(csv_file)
else:

    df_existing = pd.DataFrame(columns=["Index", "Link", "Title"])

# Base YouTube search URL
base_url = "https://www.youtube.com/results?search_query="

# Loop through each keyword
for keyword in keywords:
    search_url = f"{base_url}{keyword.replace(' ', '+')}"
    print(f"Scraping links for keyword: {keyword}")

    # Open the search page
    driver.get(search_url)

    time.sleep(3) 

    # Find all video elements (YouTube links contain '/watch?v=')
    video_elements = driver.find_elements(By.XPATH, '//a[@href]')
    video_links = []
    for elem in video_elements:
        href = elem.get_attribute("href")
        title = elem.get_attribute("title")
        print(title)

        if "/watch?v=" in href and "TED" in title:
            video_links.append({"href": href, "title": title})

    video_links = list({v["href"]: v for v in video_links}.values())

    dictionary = {index + 1: {"link": link["href"], "title": link["title"]} for index, link in enumerate(video_links)}


    df_new = pd.DataFrame.from_dict(dictionary, orient="index").reset_index()
    df_new.columns = ["Index", "Link", "Title"]

    df_existing = pd.concat([df_existing, df_new], ignore_index=True)

# Close the browser
driver.quit()

df_existing = df_existing.drop_duplicates(subset=["Link"])

df_existing.to_csv(csv_file, index=False)
print(f"All TED Talk links have been saved to {csv_file}")
