import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fpdf import FPDF
import time

url="https://notegpt.io/youtube-transcript-generator"

def init_driver():
    chrome_binary_path = '/home/malik-saad-ahmed/Desktop/Desktop/Learnings/Web Scraping/chromedriver-linux64'
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary_path
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_links(csv_file):
    df = pd.read_csv(csv_file)
    if "Link" not in df.columns:
        raise ValueError("CSV file must contain a 'Video Link' column.")
    return df["Link"].tolist()

def scrape_transcript(driver, video_link):
    driver.get(url)
    
    # Wait for the input field to load
    wait = WebDriverWait(driver, 10)
    input_field = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/header/div/div/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/div[1]/input")))

    # Enter video link
    input_field.clear()
    input_field.send_keys(video_link)
    input_field.send_keys(Keys.RETURN)

    # Wait for the transcript section to load
    time.sleep(10)

    # Parse the page source
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract transcripts
    transcripts = []
    items = soup.find_all('div', class_='ng-transcript-item')
    if items:
        for item in items:
            timestamp = item.find('div', class_='ng-transcript-item-time-a').get_text(strip=True)
            text = item.find('div', class_='text-container').get_text(strip=True)
            transcripts.append({'timestamp': timestamp, 'text': text})
    else:
        time.sleep(5)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        items = soup.find_all('div', class_='ng-transcript-item')
        for item in items:
            timestamp = item.find('div', class_='ng-transcript-item-time-a').get_text(strip=True)
            text = item.find('div', class_='text-container').get_text(strip=True)
            transcripts.append({'timestamp': timestamp, 'text': text})
    return transcripts




def save_transcripts_to_pdf(results, pdf_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def normalize_text(text):
        """Replace smart quotes and other special characters."""
        replacements = {
            "’": "'",
            "‘": "'",
            "“": '"',
            "”": '"',
            "–": "-",
            "—": "-",
            "…": "...",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    for result in results:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, f"Video Link: {result['Video Link']}", ln=True, align='L')
        pdf.ln(5)  

        transcript_text = "\n".join([f"{entry['timestamp']} {normalize_text(entry['text'])}" for entry in result['Transcript']])
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, transcript_text)
        pdf.ln(10)  

    pdf.output(pdf_filename)
    print(f"PDF saved to {pdf_filename}")



def main(input_csv, output_csv, output_pdf):
    driver = init_driver()
    video_links = load_links(input_csv)

    results = []
    for video_link in video_links:
        try:
            transcript = scrape_transcript(driver, video_link)
            results.append({"Video Link": video_link, "Transcript": transcript})
            print(f"Processed: {video_link}")
        except Exception as e:
            print(f"Failed to process {video_link}: {e}")


    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

    save_transcripts_to_pdf(results, output_pdf)

    driver.quit()

if __name__ == "__main__":
    input_csv = "ted_talk_youtube_links.csv" 
    output_csv = "ted_talk_youtube_links_transcripts.csv"  
    output_pdf = "output_transcripts.pdf"  
    main(input_csv, output_csv, output_pdf)
