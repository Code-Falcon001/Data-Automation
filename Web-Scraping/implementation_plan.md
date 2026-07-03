# AI-Assisted Job Applying System

This document outlines the phased architecture and implementation plan for building an automated, AI-assisted job scraping and application system.

## Goal Description (Phase 1)

**Phase 1 Goal**: Build an intelligent web scraper that reads your CV (or LinkedIn/Naukri profile), searches across multiple job boards, evaluates job descriptions against your profile using a local AI (OpenClaw), and consolidates only the highly matched jobs into an Excel (`.xlsx`) tracking sheet.

Future phases will handle automated form filling and Gmail outcome parsing.

## Phase 1 Architecture: AI Profile-Matching Scraper

We will build Phase 1 using Python, divided into the following core components:

### 1. Profile Ingestion & Parsing (`profile_parser.py`)
- **Inputs**: User's CV (PDF/DOCX) or structured data exported from LinkedIn/Naukri.
- **Mechanism**: Extracts the text from the CV and passes it to the **OpenClaw (kimi-k2.5:cloud)** AI.
- **Output**: The AI distills the CV into a structured set of constraints: Target Roles, Core Skills, Years of Experience, and Location constraints.

### 2. Multi-Platform Job Scraper (`job_scraper.py`)
- **Target Boards**: LinkedIn Jobs, Naukri, and select company domains.
- **Mechanism**: Uses `Selenium` or `Playwright` to search for the target roles identified by the AI. It handles pagination and extracts the Job Title, Company, Location, Job URL, and the full Job Description (JD) text.

### 3. AI JD Matcher (`ai_matcher.py`)
- **Mechanism**: For every scraped job, the script sends the JD and your structured profile to the local OpenClaw AI.
- **Evaluation**: The AI acts as a recruiter, evaluating if your profile matches the JD requirements. It returns a `Match Score (0-100)` and a brief `Match Reason`.

### 4. Excel Consolidator (`excel_manager.py`)
- **Mechanism**: Uses `pandas` to filter out jobs below a certain match threshold (e.g., < 70%).
- **Output Setup**: Saves the matched jobs into a master Excel tracker (`job_applications.xlsx`).
- **Data Fields**: Job Title, Company, URL, Location, Match Score, Match Reason, Snapshot Date (Date of scraping), Status ('Pending').

## Open Questions for Phase 1

1. **Profile Input Method**: To start phase 1, would you prefer to just place a `CV.pdf` in the folder for the script to analyze, or do you want the script to try logging into Naukri/LinkedIn to pull your profile directly? (Using a `.pdf` is much faster to build and less prone to anti-bot blocks).
2. **AI Matching Threshold**: Do you want the Excel sheet to include *all* scraped jobs with their match scores, or strictly only the ones that the AI deems a "Strong Match"?

## Verification Plan (Phase 1)
- **Profile Test**: Ensure the script correctly pulls text from your CV and OpenClaw successfully identifies your skills and experience.
- **Scraping Test**: Verify the scraper can extract 20+ JDs from LinkedIn/Naukri without being blocked.
- **Matching Test**: Review the final `job_applications.xlsx` to confirm the AI accurately scored the jobs based on your actual CV text.
