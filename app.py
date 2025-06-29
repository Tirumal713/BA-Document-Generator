"""
Streamlit frontend for the CrewAI Multi-Agent Project Documentation System.
This app allows users to upload media files, process them, and view generated documentation.
"""
import os
import time
import base64
import requests
import streamlit as st
from typing import Dict, Any, Optional, List

# Set Streamlit port
os.environ['STREAMLIT_SERVER_PORT'] = '8502'

# API Configuration
API_BASE_URL = "http://localhost:7000"

# Set page config
st.set_page_config(
    page_title="CrewAI Project Documentation Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .pdf-viewer {
        width: 100%;
        height: 800px;
        border: none;
    }
    .download-btn {
        margin-top: 10px;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        margin-bottom: 0.5rem;
    }
    .stAlert {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Helper functions
def upload_and_process_file(uploaded_file, doc_type="BRD", doc_level="Intermediate"):
    """Upload a file to the API and start processing."""
    try:
        # Create a files dictionary for the request
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        # Log the upload attempt
        st.write(f"Attempting to upload file: {uploaded_file.name} ({uploaded_file.size} bytes)")
        st.write(f"Document type: {doc_type}")
        st.write(f"Documentation level selected: {doc_level}")
        
        # Make the API request with documentation type and level parameters
        response = requests.post(
            f"{API_BASE_URL}/upload", 
            files=files,
            data={
                "doc_type": doc_type,
                "doc_level": doc_level
            }
        )
        
        # Log the response status
        st.write(f"Upload response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            st.write(f"Response content: {result}")
            
            if result.get("success"):
                st.write(f"File ID: {result.get('file_id')}")
                return result
            else:
                st.error(f"Upload failed: {result.get('message', 'Unknown error')}")
                return None
        else:
            st.error(f"Upload failed with status code {response.status_code}")
            try:
                st.write(f"Error details: {response.json()}")
            except:
                st.write("Could not parse error response")
            return None
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return None

def check_documentation_exists(file_id):
    """Check if documentation exists for the given file ID."""
    try:
        st.write(f"Checking if documentation exists for file ID: {file_id}")
        response = requests.get(f"{API_BASE_URL}/documentation/{file_id}")
        st.write(f"Documentation check status code: {response.status_code}")
        
        if response.status_code == 200:
            st.write("Documentation exists!")
            return True
        else:
            st.write(f"Documentation not ready yet. Status: {response.status_code}")
            # Also check processing status
            try:
                status_response = requests.get(f"{API_BASE_URL}/status/{file_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    st.write(f"Processing status: {status_data.get('status')}")
                    st.write(f"Progress: {status_data.get('progress')}%")
                    st.write(f"Current stage: {status_data.get('current_stage')}")
                    if status_data.get('error'):
                        st.error(f"Processing error: {status_data.get('error')}")
            except Exception as status_err:
                st.write(f"Could not get processing status: {str(status_err)}")
            return False
    except Exception as e:
        st.write(f"Error checking documentation: {str(e)}")
        return False

def get_pdf_content(file_id):
    """Get PDF content for the given file ID."""
    try:
        response = requests.get(f"{API_BASE_URL}/download/{file_id}?format=pdf")
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

def get_document_download_url(file_id, format="pdf"):
    """Get download URL for the document."""
    return f"{API_BASE_URL}/download/{file_id}?format={format}"

def display_pdf(pdf_content):
    """Display PDF content in an iframe."""
    base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" class="pdf-viewer"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def create_download_button(file_id, format, label):
    """Create a download button for the document."""
    download_url = get_document_download_url(file_id, format)
    st.markdown(
        f'<div class="download-btn"><a href="{download_url}" target="_blank">'
        f'<button style="width:100%;padding:0.5em;background-color:#4CAF50;color:white;'
        f'border:none;border-radius:5px;cursor:pointer;">'
        f'{label}</button></a></div>',
        unsafe_allow_html=True
    )

# Main app
st.title("📄 CrewAI Project Documentation Generator")
st.markdown("---")

# Sidebar
st.sidebar.title("Upload Media")
st.sidebar.markdown("Upload audio or video files to generate project documentation.")

# Document type selection
doc_type = st.sidebar.selectbox(
    "Select Document Type",
    options=["BRD", "SOW", "FRD"],
    help="Choose the type of document you want to generate."
)

# Display information about the selected document type
if doc_type == "BRD":
    st.sidebar.info("Business Requirements Document (BRD): Defines the business needs and requirements for a project.")
elif doc_type == "SOW":
    st.sidebar.info("Statement of Work (SOW): Details the specific work to be performed, deliverables, and timeline.")
elif doc_type == "FRD":
    st.sidebar.info("Functional Requirements Document (FRD): Specifies the functional requirements and system behavior.")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "Choose a media file",
    type=["mp3", "wav", "mp4", "avi", "mov", "m4a", "ogg"],
    help="Upload an audio or video file to generate documentation."
)

# Documentation level dropdown
if uploaded_file is not None:
    st.sidebar.markdown("### Select Documentation Level")
    doc_level = st.sidebar.selectbox(
        "Select Documentation Level",
        options=["Simple", "Intermediate", "Advanced"],
        help="Choose the level of detail for your document."
    )
    
    # Display information about the selected level
    if doc_level == "Simple":
        st.sidebar.info("Simple: Concise document with fundamental project information. Suitable for initial discussions.")
    elif doc_level == "Intermediate":
        st.sidebar.info("Intermediate: Detailed document with comprehensive requirements and process flows. Suitable for project development.")
    elif doc_level == "Advanced":
        st.sidebar.info("Advanced: Exhaustive document with in-depth analysis and specifications. Suitable for complex enterprise projects.")

# Process file button
if uploaded_file is not None:
    if st.sidebar.button("Process File"):
        with st.spinner("Uploading and processing file..."):
            result = upload_and_process_file(uploaded_file, doc_type, doc_level)
            if result:
                file_id = result.get("file_id")
                st.session_state.uploaded_files.append({
                    "file_id": file_id,
                    "filename": uploaded_file.name,
                    "doc_type": doc_type,
                    "doc_level": doc_level,
                    "upload_time": time.time()
                })
                st.success(f"File uploaded successfully! File ID: {file_id}")

# Display uploaded files and documentation
st.header("Generated Documentation")

if not st.session_state.uploaded_files:
    st.info("No files have been uploaded yet. Upload a file to get started.")
else:
    # Refresh status button
    if st.button("Refresh Status"):
        st.experimental_rerun()
    
    # Display each uploaded file and its documentation
    for file_info in st.session_state.uploaded_files:
        file_id = file_info["file_id"]
        filename = file_info["filename"]
        
        st.subheader(f"File: {filename}")
        st.markdown(f"File ID: `{file_id}`")
        
        # Check if documentation exists
        if check_documentation_exists(file_id):
            # Get PDF content
            pdf_content = get_pdf_content(file_id)
            if pdf_content:
                # Create download buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    create_download_button(file_id, "pdf", "Download PDF")
                with col2:
                    create_download_button(file_id, "docx", "Download DOCX")
                with col3:
                    create_download_button(file_id, "html", "Download HTML")
                with col4:
                    create_download_button(file_id, "json", "Download JSON")
                
                # Display PDF
                st.markdown("### PDF Preview")
                display_pdf(pdf_content)
            else:
                st.warning("PDF content not available. Try refreshing.")
        else:
            with st.spinner("Documentation is being generated..."):
                st.info("Documentation is not ready yet. Please wait or refresh.")
