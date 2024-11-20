import streamlit as st
import pandas as pd
from utils.file_handler import FileHandler
from utils.search_handler import SearchHandler
from utils.llm_handler import LLMHandler
from config.config import load_config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Data Extraction Tool",
        page_icon="🤖",
        layout="wide"
    )
    
    # Page title
    st.title("🤖 AI Agent - Data Extraction Tool")
    
    # Sidebar for configurations
    with st.sidebar:
        st.header("⚙️ Configuration")
        model_name = st.selectbox(
            "Select Language Model:",
            [
                "meta-llama/Llama-2-7b-chat-hf",
                "facebook/opt-1.3b",
                "google/flan-t5-large",
                "microsoft/phi-1_5"
            ],
            help="Choose the model for information extraction"
        )
    
    # Initialize handlers with proper error handling
    file_handler = FileHandler()
    search_handler = SearchHandler()
    
    # Load LLM model with error handling
    llm_handler = None
    with st.spinner("Loading language model..."):
        try:
            llm_handler = LLMHandler(model_name=model_name)
            st.success(f"✅ Model {model_name} loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            st.info("Please select a different model from the sidebar.")
            return
    
    # File upload section
    st.header("1. Data Input 📁")
    upload_type = st.radio(
        "Choose input method:",
        ["CSV Upload", "Google Sheets"],
        horizontal=True
    )
    
    df = None  # Will store uploaded data
    
    # File upload or Google Sheets handling
    if upload_type == "CSV Upload":
        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=['csv'],
            help="Upload a CSV file containing the data to process"
        )
        if uploaded_file:
            df = file_handler.process_csv(uploaded_file)
    else:
        sheet_url = st.text_input(
            "Enter Google Sheet URL:",
            help="Provide the sharing URL of your Google Sheet"
        )
        if sheet_url:
            if not sheet_url.startswith("https://docs.google.com/spreadsheets/"):
                st.error("Invalid Google Sheets URL. Please provide a valid URL.")
            else:
                df = file_handler.process_google_sheet(sheet_url)
    
    # If data is successfully loaded, proceed
    if df is not None:
        st.success("✅ Data loaded successfully!")
        st.subheader("Preview of loaded data")
        st.dataframe(df.head(), use_container_width=True)
        
        # Search configuration
        st.header("2. Configure Search 🔍")
        col1, col2 = st.columns(2)
        with col1:
            selected_column = st.selectbox(
                "Select the main column for search:",
                df.columns,
                help="Choose the column containing entities to search for"
            )
        with col2:
            prompt_template = st.text_area(
                "Enter your search prompt template:",
                "Get me the email address of {entity}",
                help="Use {entity} as a placeholder for the value from your selected column"
            )
        
        # Start processing data
        if st.button("🚀 Start Processing", type="primary", use_container_width=True):
            st.warning("⚠️ Processing might take several minutes depending on data size and the selected model.")
            
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_placeholder = st.empty()
                
                results = []  # Store results
                total_rows = len(df)
                
                for index, row in df.iterrows():
                    entity = str(row[selected_column])  # Ensure entity is a string
                    status_text.text(f"🔄 Processing {entity} ({index + 1}/{total_rows})...")
                    
                    try:
                        search_results = search_handler.search(entity, prompt_template)
                        extracted_info = (
                            "No search results found"
                            if not search_results
                            else llm_handler.extract_information(search_results, entity, prompt_template)
                        )
                        
                        results.append({
                            'Entity': entity,
                            'Extracted Information': extracted_info
                        })
                        temp_df = pd.DataFrame(results)
                        results_placeholder.dataframe(temp_df, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error processing {entity}: {str(e)}")
                        results.append({
                            'Entity': entity,
                            'Extracted Information': f"Error during processing: {str(e)}"
                        })
                    
                    progress_bar.progress((index + 1) / total_rows)
                
                status_text.text("✅ Processing complete!")
            
            # Display results
            st.header("3. Results 📊")
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Export options
            st.subheader("Export Options")
            col1, col2 = st.columns(2)
            with col1:
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="extracted_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col2:
                if upload_type == "Google Sheets" and sheet_url:
                    if st.button("🔄 Update Google Sheet"):
                        try:
                            file_handler.update_google_sheet(sheet_url, results_df)
                            st.success("✅ Google Sheet updated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error updating Google Sheet: {str(e)}")

if __name__ == "__main__":
    main()
