from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import urllib.parse
from config import TARGET_JOB_COUNT
import logging

def scrape_linkedin(p, query):
    """Scrapes public facing LinkedIn Jobs."""
    jobs = []
    encoded_query = urllib.parse.quote(query)
    url = f"https://in.linkedin.com/jobs/search?keywords={encoded_query}&location=India&f_TPR=r2592000" # Last 30 days
    
    try:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        logging.info(f"Navigating to LinkedIn Jobs to search for {query}...")
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3000) # Let React hydrate
        
        # Scroll logic to load more jobs
        for _ in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        job_cards = soup.select('ul.jobs-search__results-list li')
        for idx, card in enumerate(job_cards):
            if len(jobs) >= TARGET_JOB_COUNT // 2: # Give 50% to this scraper
                break
                
            title_elem = card.select_one('h3.base-search-card__title')
            company_elem = card.select_one('h4.base-search-card__subtitle')
            location_elem = card.select_one('span.job-search-card__location')
            link_elem = card.select_one('a.base-card__full-link')
            
            title = title_elem.text.strip() if title_elem else "Unknown Title"
            company = company_elem.text.strip() if company_elem else "Unknown Company"
            location = location_elem.text.strip() if location_elem else "India"
            job_url = link_elem.get('href', '').split('?')[0] if link_elem else "" # remove tracking query params
            
            # Since LinkedIn Public blocks deep scraping heavily, we will rely on snippets if available, or just the title/company.
            # Usually extracting full JD from linkedin public without login requires hitting the url directly
            jd_text = f"Target Role: {title}\nCompany: {company}\nLocation: {location}\nNote: LinkedIn specific JD requires direct navigation. Use title and company context for matching."
            
            if title != "Unknown Title":
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": job_url,
                    "jd": jd_text
                })
        browser.close()
    except Exception as e:
        logging.error(f"LinkedIn scraping failed: {e}")
    return jobs

def scrape_google_careers(p, query):
    """Scrapes Google Careers."""
    jobs = []
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/about/careers/applications/jobs/results?q={encoded_query}&location=India"
    
    try:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        logging.info(f"Navigating to Google Careers to search for {query}...")
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(2000)
        
        cards_count = page.locator('div[jscontroller="eH4Yic"]').count()
        
        for index in range(min(cards_count, TARGET_JOB_COUNT // 2)):
            card = page.locator('div[jscontroller="eH4Yic"]').nth(index)
            title = card.locator('h2').inner_text() if card.locator('h2').count() > 0 else "Unknown Title"
            location = card.locator('.RP7SMd span').first.inner_text() if card.locator('.RP7SMd span').count() > 0 else "India"
            
            # Fetch snippet
            jd_text = ""
            if card.locator('.ObfsIf-eMeQre').count() > 0:
                jd_text = card.locator('.ObfsIf-eMeQre').first.inner_text()
                
            jobs.append({
                "title": title,
                "company": "Google",
                "location": location,
                "url": url,
                "jd": f"Google Role: {title}. Location: {location}. Details: {jd_text}"
            })
        browser.close()
    except Exception as e:
        logging.error(f"Google Careers scraping failed: {e}")
    return jobs

def search_jobs(target_roles):
    """
    Main orchestrator for scraping multiple sources safely.
    """
    if not target_roles:
        logging.warning("No target roles to search for.")
        return []
        
    query = target_roles[0] 
    found_jobs = []
    
    with sync_playwright() as p:
        # Aggregating jobs from multiple sources
        linkedin_jobs = scrape_linkedin(p, query)
        google_jobs = scrape_google_careers(p, query)
        
        found_jobs.extend(linkedin_jobs)
        found_jobs.extend(google_jobs)
        
    # Optional logic: Deduplicate by exact URL (ExcelManager also handles this)
    return found_jobs

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    jobs = search_jobs(["Data Engineer"])
    print(f"Found {len(jobs)} jobs.")
    for j in jobs:
        print(j["title"], "-", j["company"])
