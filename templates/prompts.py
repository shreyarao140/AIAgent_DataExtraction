# 1. templates/prompts.py
class PromptTemplates:
    # Basic search templates
    SEARCH_TEMPLATES = {
        "email": "Get me the email address of {entity}",
        "phone": "Find the phone number for {entity}",
        "linkedin": "Find the LinkedIn profile URL for {entity}",
        "company": "Find the current company and role of {entity}",
        "social_media": "Find social media profiles for {entity}",
        "website": "Find the personal or professional website of {entity}",
    }
    
    # LLM extraction templates
    EXTRACTION_TEMPLATES = {
        "email": """
        Based on the following search results about {entity}, extract their email address:
        
        Search Results:
        {context}
        
        Please provide only the email address. If multiple addresses are found, list all.
        If no email is found, respond with "No email found."
        """,
        
        "contact_info": """
        Based on the following search results about {entity}, extract their contact information:
        
        Search Results:
        {context}
        
        Please extract and format the following information:
        - Email: 
        - Phone:
        - Location:
        - Current Role:
        - Company:
        
        For any information not found, write "Not found".
        """,
        
        "professional_info": """
        Based on the following search results about {entity}, extract their professional information:
        
        Search Results:
        {context}
        
        Please extract and format the following:
        - Current Position:
        - Company:
        - Industry:
        - Experience:
        - Education:
        - Skills:
        
        For any information not found, write "Not found".
        """
    }
    
    @classmethod
    def get_search_template(cls, template_name):
        """Get a search template by name"""
        return cls.SEARCH_TEMPLATES.get(template_name)
    
    @classmethod
    def get_extraction_template(cls, template_name):
        """Get an extraction template by name"""
        return cls.EXTRACTION_TEMPLATES.get(template_name)
    
    @classmethod
    def get_available_templates(cls):
        """Get list of all available template names"""
        return {
            "search": list(cls.SEARCH_TEMPLATES.keys()),
            "extraction": list(cls.EXTRACTION_TEMPLATES.keys())
        }

