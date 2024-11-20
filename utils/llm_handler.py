from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import streamlit as st

class LLMHandler:
    def __init__(self, model_name="facebook/opt-1.3b"):  # Changed default model to a more reliable one
        try:
            # Initialize tokenizer first
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Initialize model with proper configuration
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_8bit=True  # Use 8-bit quantization for better memory usage
            )
            
            # Set up the generation configuration
            self.model.config.pad_token_id = self.tokenizer.pad_token_id
            self.model.config.eos_token_id = self.tokenizer.eos_token_id
            
            print(f"Model {model_name} initialized successfully.")
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            raise e

    def generate_text(self, prompt, max_length=500):
        """Generate text using the model with improved error handling"""
        try:
            # Tokenize with proper padding and truncation
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length
            ).to(self.model.device)
            
            # Generate with carefully tuned parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    min_length=50,  # Ensure some minimum content
                    num_return_sequences=1,
                    temperature=0.7,
                    top_p=0.95,
                    top_k=50,
                    do_sample=True,
                    no_repeat_ngram_size=2,
                    early_stopping=True
                )
            
            # Decode the generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up the response
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return generated_text if generated_text else "No relevant information found"

        except Exception as e:
            print(f"Error during text generation: {str(e)}")
            return "Information could not be extracted. Please try again."

    def extract_information(self, search_results, entity, prompt_template):
        """Extract information with improved prompt engineering"""
        try:
            # Format search results into a clear, structured context
            context_parts = []
            for i, result in enumerate(search_results, 1):
                context_parts.append(f"""
Source {i}:
Title: {result.get('title', 'No title')}
Content: {result.get('snippet', 'No content')}
URL: {result.get('link', 'No URL')}
""")
            
            context = "\n".join(context_parts)

            # Create a more focused extraction prompt
            extraction_prompt = f"""
Given the search results below, extract the requested information about {entity}.
Search Query: {prompt_template.format(entity=entity)}

Search Results:
{context}

Instructions:
1. Focus on finding specific, factual information
2. If multiple sources provide different information, mention the discrepancy
3. If no relevant information is found, clearly state that
4. Format the response in a clear, concise manner

Please provide the extracted information:
"""

            # Generate response with structured prompt
            extracted_info = self.generate_text(extraction_prompt)
            
            # Clean up and validate response
            cleaned_response = extracted_info.strip()
            if not cleaned_response or cleaned_response.lower() in ['none', 'no information found']:
                return f"No specific information found for {entity}"
                
            return cleaned_response
        
        except Exception as e:
            print(f"Error during information extraction: {str(e)}")
            return f"Unable to process information for {entity}"

    def _format_response(self, text):
        """Helper method to format and clean responses"""
        # Remove any leading/trailing whitespace and quotes
        text = text.strip().strip('"\'')
        
        # Remove any repeated newlines
        text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
        
        # If the response is too short or seems invalid
        if len(text) < 10:
            return "No specific information found"
            
        return text