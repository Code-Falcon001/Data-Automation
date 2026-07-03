import pandas as pd
import os
import csv
from config import EXCEL_TRACKER_PATH
from datetime import datetime
import logging

class ExcelManager:
    def __init__(self):
        self.file_path = EXCEL_TRACKER_PATH
        self.columns = [
            "Job Title", 
            "Company", 
            "Location", 
            "Job URL", 
            "Match Score", 
            "Match Reason", 
            "Snapshot Date", 
            "Status"
        ]
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            try:
                df = pd.DataFrame(columns=self.columns)
                df.to_excel(self.file_path, index=False, engine='openpyxl')
            except PermissionError:
                logging.error(f"Cannot create {self.file_path}. Is it open in another program?")

    def add_job_entry(self, job_data):
        if "Snapshot Date" not in job_data:
            job_data["Snapshot Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "Status" not in job_data:
            job_data["Status"] = "Pending"
            
        try:
            df = pd.read_excel(self.file_path, engine='openpyxl')
        except Exception as e:
            logging.error(f"Error reading Excel sheet: {e}")
            return False
            
        if job_data["Job URL"] in df["Job URL"].values:
            logging.info(f"Skipping tracked job: {job_data['Job URL'][:50]}...")
            return False
            
        new_row_df = pd.DataFrame([job_data])
        df = pd.concat([df, new_row_df], ignore_index=True)
        
        try:
            df.to_excel(self.file_path, index=False, engine='openpyxl')
            return True
        except PermissionError:
            logging.error(f"Cannot write to {self.file_path}. Is it open in Microsoft Excel? Please close it.")
            return False
        except Exception as e:
            logging.error(f"Failed to save Excel file: {e}")
            return False
