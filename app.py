import streamlit as st
import chat
import quiz
import dashboard
import login
import database
from utils import load_css

# ✅ Ensure all required session state variables are initialized before anything else
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "quiz_questions" not in st.session_state:
    st.session_state["quiz_questions"] = []

if "quiz_started" not in st.session_state:
    st.session_state["quiz_started"] = False

if "quiz_finished" not in st.session_state:
    st.session_state["quiz_finished"] = False

if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ✅ Load custom CSS for styling
load_css()

# ✅ Ensure authentication before showing the app
if not st.session_state["authenticated"]:
    login.show_login()
    st.stop()

# ✅ Show the different sections of the app
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Chat", "Quiz", "Dashboard"])

if page == "Chat":
    chat.chat_ui()

elif page == "Quiz":
    quiz.quiz_ui()

elif page == "Dashboard":
    dashboard.performance_dashboard()

st.title("📚 AI Tutor with Adaptive Learning")

# ✅ Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login.show_login()
    st.stop()
