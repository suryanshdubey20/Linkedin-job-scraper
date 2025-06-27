from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import os

def scrape_linkedin_jobs(search_keyword="Python Developer", location="India", max_jobs=10):
    # ✅ ChromeDriver path setup
    driver_path = os.path.abspath("driver/chromedriver.exe")
    service = Service(driver_path)

    # ✅ Chrome browser settings
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run invisibly
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # ✅ LinkedIn jobs search URL
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_keyword}&location={location}"
    driver.get(search_url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "base-search-card__title"))
        )
        print("✅ Job listings loaded!")
    except:
        print("❌ Failed to load job listings.")
        driver.quit()
        return []

    # ✅ Parse job cards
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("div", class_="base-card")

    job_data = []
    for job in job_cards[:max_jobs]:
        try:
            title = job.find("h3", class_="base-search-card__title").text.strip()
            company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            link = job.find("a", class_="base-card__full-link")["href"]
            job_data.append({
                "title": title,
                "company": company,
                "link": link
            })
        except:
            continue

    driver.quit()
    return job_data

# ✅ Run the scraper
if __name__ == "__main__":
    jobs = scrape_linkedin_jobs("Data Scientist", "India", 10)

    # ✅ Print to terminal
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Link: {job['link']}")

    # ✅ Save to new JSON file (jobs_1.json, jobs_2.json, ...)
    i = 1
    while os.path.exists(f"jobs_{i}.json"):
        i += 1

    filename = f"jobs_{i}.json"
    with open(filename, "w") as f:
        json.dump(jobs, f, indent=4)
        print(f"📁 Saved to {filename}")


         
