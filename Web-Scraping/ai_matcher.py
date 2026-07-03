import requests
import json
import re
import time
import logging
from config import OPENCLAW_API_BASE, OPENCLAW_MODEL, OPENCLAW_API_KEY

def evaluate_job_match(profile_data, job_description):
    prompt = f"""
    You are an expert technical recruiter matching a candidate to a job.
    
    Candidate Profile:
    ---
    {json.dumps(profile_data, indent=2)}
    ---
    
    Job Description:
    ---
    {job_description[:3500]} # Limit JD length for local models constraint
    ---
    
    Evaluate the candidate's fit for this role based on their skills and experience versus the requirements.
    Return ONLY a valid JSON object with EXACTLY two keys:
    - "match_score": an integer representing the fit (0-100).
    - "match_reason": a short explanation of why this score was given.
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
    
    for attempt in range(3):
        try:
            response = requests.post(f"{OPENCLAW_API_BASE}/chat/completions", headers=headers, json=payload, timeout=60)
            if response.status_code != 200:
                logging.error(f"OpenClaw API Error: {response.status_code} - {response.text}")
                response.raise_for_status()
                
            data = response.json()
            raw_content = data['choices'][0]['message']['content']
            
            # Robust JSON extraction
            json_match = re.search(r'\{.*\}', raw_content.strip(), re.DOTALL)
            if not json_match:
                raise ValueError("No JSON object found in AI response.")
                
            result_json = json.loads(json_match.group(0))
            
            # Robust type casting
            try:
                score = int(float(result_json.get("match_score", 0)))
            except:
                score = 0
                
            return {
                "Match Score": score,
                "Match Reason": str(result_json.get("match_reason", "No reason provided."))
            }
            
        except Exception as e:
            logging.warning(f"AI Evaluation attempt {attempt+1} failed: {e}")
            time.sleep(2)
            
    return {"Match Score": 0, "Match Reason": "Failed to evaluate after 3 API retries."}
