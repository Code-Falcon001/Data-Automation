import fitz  # PyMuPDF
import requests
import json
import re
import time
import logging
from config import CV_PATH, OPENCLAW_API_BASE, OPENCLAW_MODEL, OPENCLAW_API_KEY
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Could not find CV at {pdf_path}")
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
    return text.strip()

def build_structured_profile(cv_text):
    prompt = f"""
    You are an expert recruiter. I am providing you with the raw text of a candidate's CV.
    Your task is to extract the core professional profile into a JSON format.
    
    Extract the following fields:
    - "current_role": A short string describing their most recent/current job title.
    - "years_of_experience": Best estimate of total professional years of experience (number).
    - "core_skills": A list of the top technical skills.
    - "target_roles": A list of 3-5 job titles they would be highly suited for.
    
    CV TEXT:
    ---
    {cv_text[:3000]}
    ---
    
    Return ONLY a valid JSON object.
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENCLAW_API_KEY}"
    }
    
    payload = {
        "model": OPENCLAW_MODEL,
        "messages": [
            {"role": "system", "content": "You output only structured JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    logging.info("Calling OpenClaw AI to parse profile...")
    for attempt in range(3):
        try:
            response = requests.post(f"{OPENCLAW_API_BASE}/chat/completions", headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            raw_content = data['choices'][0]['message']['content']
            
            # Robust JSON extraction
            json_match = re.search(r'\{.*\}', raw_content.strip(), re.DOTALL)
            if not json_match:
                raise ValueError("No JSON object found in AI response.")
                
            profile_json = json.loads(json_match.group(0))
            return profile_json
        except Exception as e:
            logging.warning(f"Profile API attempt {attempt+1} failed: {e}")
            time.sleep(2)
            
    # Fallback
    return {
        "current_role": "Unknown",
        "years_of_experience": 0,
        "core_skills": [],
        "target_roles": []
    }
