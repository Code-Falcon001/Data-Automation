from profile_parser import extract_text_from_pdf, build_structured_profile
from job_scraper import search_jobs
from ai_matcher import evaluate_job_match
from excel_manager import ExcelManager
from config import CV_PATH, MIN_MATCH_SCORE
import sys
import json
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logging.info("--- AI Job Applicator (Phase 1) ---")
    
    try:
        # 1. Parse CV
        logging.info("Step 1: Parsing CV & Extracting Profile...")
        cv_text = extract_text_from_pdf(CV_PATH)
        if not cv_text:
            logging.error("Cannot proceed without CV text. Please ensure CV.pdf exists.")
            sys.exit(1)
            
        profile = build_structured_profile(cv_text)
        logging.info("Parsed Profile Highlights:")
        print(json.dumps(profile, indent=2))
        
        # 2. Scrape Jobs
        target_roles = profile.get("target_roles", ["IT Professional"])
        if not target_roles:
            target_roles = ["IT Professional"]
            
        logging.info("Step 2: Scraping Job Boards (Multi-Source)...")
        scraped_jobs = search_jobs(target_roles)
        logging.info(f"Successfully scraped {len(scraped_jobs)} jobs.")
        
        if not scraped_jobs:
            logging.warning("No jobs found. Exiting.")
            sys.exit(0)
            
        # 3. Match and Evaluate
        logging.info("Step 3: Evaluating Matches with OpenClaw...")
        excel_manager = ExcelManager()
        
        processed_count = 0
        saved_count = 0
        
        for job in scraped_jobs:
            if not job.get("jd"):
                continue
                
            logging.info(f"Evaluating {job['title']} at {job['company']}")
            match_result = evaluate_job_match(profile, job["jd"])
            
            score = match_result.get("Match Score", 0)
            reason = match_result.get("Match Reason", "N/A")
            
            logging.info(f"  -> Match Score: {score}/100")
            print(f"     Reason: {reason}")
            
            if score >= MIN_MATCH_SCORE:
                entry = {
                    "Job Title": job["title"],
                    "Company": job["company"],
                    "Location": job["location"],
                    "Job URL": job["url"],
                    "Match Score": score,
                    "Match Reason": reason
                }
                success = excel_manager.add_job_entry(entry)
                if success:
                    saved_count += 1
                    
            processed_count += 1
            
        logging.info("--- Process Complete ---")
        logging.info(f"Evaluated {processed_count} jobs.")
        logging.info(f"Saved {saved_count} jobs to tracking system.")
        
    except Exception as e:
        logging.critical(f"A critical error disrupted the pipeline: {e}")

if __name__ == "__main__":
    main()
