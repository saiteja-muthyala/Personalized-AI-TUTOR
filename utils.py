import os
import json
import fitz  # PyMuPDF for PDF processing
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_users(user_file="users.json"):
    """Load users from a JSON file."""
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            return json.load(f)
    return {}

def save_users(users, user_file="users.json"):
    """Save users to a JSON file."""
    with open(user_file, "w") as f:
        json.dump(users, f, indent=4)

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    text = ""
    if uploaded_file is not None:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    return text

# ✅ Streamlit File Uploader
uploaded_pdf = st.file_uploader("📂 Upload a PDF", type=["pdf"])

if uploaded_pdf:
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.session_state["pdf_text"] = pdf_text  # Store in session state
    st.success(f"✅ PDF '{uploaded_pdf.name}' uploaded successfully!")
    st.write("📄 Extracted Text Preview:")
    st.text_area("Extracted Text", pdf_text[:500], height=200)

def initialize_session_keys():
    """Ensure all session state keys are initialized."""
    keys = ["chat_history", "quiz_questions", "quiz_started", "quiz_finished"]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = [] if "history" in key or "questions" in key else False

def load_css():
    """Loads and applies styles.css file"""
    css_file = "styles.css"
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error("❌ styles.css file not found! Ensure it exists in your project directory.")