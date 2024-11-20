import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import streamlit as st

class FileHandler:
    def __init__(self):
        # Set up Google Sheets when created
        self.setup_google_credentials()
    
    def setup_google_credentials(self):
        # Try to set up Google Sheets access
        try:
            # Get Google credentials from Streamlit secrets
            self.credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"]
            )
            # Create Google Sheets service
            self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        except Exception as e:
            st.warning("Google Sheets integration not configured")
    
    def process_csv(self, file):
        """Handles CSV file uploads"""
        try:
            # Read CSV file into a pandas DataFrame
            return pd.read_csv(file)
        except Exception as e:
            st.error(f"Error processing CSV file: {str(e)}")
            return None
    
    def process_google_sheet(self, sheet_url):
        """Handles Google Sheets data"""
        try:
            # Get the sheet ID from the URL
            sheet_id = sheet_url.split('/')[-2]
            
            # Read the sheet data
            range_name = 'Sheet1!A:Z'  # Read all columns
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()
            
            # Get the values from the sheet
            values = result.get('values', [])
            if not values:
                st.error('No data found in Google Sheet')
                return None
                
            # Convert to DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            return df
            
        except Exception as e:
            st.error(f"Error processing Google Sheet: {str(e)}")
            return None
    
    def update_google_sheet(self, sheet_url, results_df):
        """Updates Google Sheet with results"""
        try:
            # Get sheet ID from URL
            sheet_id = sheet_url.split('/')[-2]
            
            # Prepare data for update
            values = [results_df.columns.tolist()] + results_df.values.tolist()
            
            body = {
                'values': values
            }
            
            # Update the sheet
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range='Results!A1',  # Put results in new 'Results' sheet
                valueInputOption='RAW',
                body=body
            ).execute()
            
        except Exception as e:
            st.error(f"Error updating Google Sheet: {str(e)}")