from serpapi import Client
import os
import streamlit as st
from time import sleep

class SearchHandler:
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_KEY')
        if not self.api_key:
            st.error("SerpAPI key not found in environment variables")
        self.client = Client(api_key=self.api_key)
    
    def search(self, entity, prompt_template):
        """Performs web searches for information"""
        try:
            query = prompt_template.format(entity=entity)
            
            # Use the new SerpAPI Client
            results = self.client.search({
                "engine": "google",
                "q": query,
                "num": 5,
                "hl": "en",
                "gl": "us"
            })
            
            extracted_results = []
            if 'organic_results' in results:
                for result in results['organic_results']:
                    extracted_results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', '')
                    })
            
            # Add a small delay to respect rate limits
            sleep(1)
            
            return extracted_results
            
        except Exception as e:
            st.error(f"Error during search: {str(e)}")
            return []