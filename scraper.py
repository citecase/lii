import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "http://www.commonlii.org/in/cases/INSC/"
START_YEAR = 1950
END_YEAR = 2024

def scrape_to_markdown():
    os.makedirs("cases", exist_ok=True)

    for year in range(START_YEAR, END_YEAR + 1):
        year_url = f"{BASE_URL}{year}/"
        print(f"Processing {year}...")
        
        try:
            response = requests.get(year_url, timeout=15)
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            
            md_content = f"# Supreme Court of India Cases - {year}\n\n"
            md_content += "| Case Name | Citation | Link |\n"
            md_content += "|-----------|----------|------|\n"
            
            count = 0
            for link in links:
                href = link.get('href')
                if href and href.endswith('.html') and 'index.html' not in href:
                    full_link = f"{year_url}{href}"
                    text = link.get_text(strip=True)
                    
                    name = text.split('[')[0].strip() if '[' in text else text
                    cite = text.split('[')[1].split(']')[0].strip() if '[' in text else "N/A"
                    
                    md_content += f"| {name} | {cite} | [View Case]({full_link}) |\n"
                    count += 1
            
            if count > 0:
                with open(f"cases/{year}.md", "w", encoding="utf-8") as f:
                    f.write(md_content)
                print(f"  Saved {count} cases to cases/{year}.md")
            
            time.sleep(1) # Be gentle on CommonLII servers

        except Exception as e:
            print(f"  Error in {year}: {e}")

if __name__ == "__main__":
    scrape_to_markdown()
