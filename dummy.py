import os
import json
import sqlite3
import streamlit as st
import fitz  
import groq
import re
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ Updated Import

# ✅ Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY! Please set it in .env.")

# ✅ Initialize AI
client = groq.Client(api_key=GROQ_API_KEY)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Set up SQLite database
conn = sqlite3.connect("ai_tutor.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER,
        total_questions INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# ✅ Ensure all session state keys are initialized
for key, default in {
    "chat_history": [],
    "quiz_questions": [],
    "quiz_started": False,
    "quiz_finished": False,
    "pdf_text": "",
    "authenticated": False,
    "score": 0,
    "user_answers": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ✅ User Authentication System
USER_FILE = "users.json"

def load_users():
    """Load users from a JSON file."""
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to a JSON file."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def login():
    """Login system for the AI tutor."""
    st.sidebar.title("🔐 User Login")
    users = load_users()

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if username in users and users[username]["password"] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.sidebar.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid Username or Password")

def signup():
    """Signup system for new users."""
    st.sidebar.subheader("Create a New Account")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    signup_button = st.sidebar.button("Signup")

    if signup_button:
        users = load_users()
        if new_username in users:
            st.sidebar.error("❌ Username already exists!")
        else:
            users[new_username] = {"password": new_password}
            save_users(users)
            st.sidebar.success("✅ Account created! Please log in.")

# ✅ Ensure user authentication before accessing the tutor
if not st.session_state["authenticated"]:
    login()
    signup()
    st.stop()

# ✅ Streamlit UI
st.title("📚 AI Tutor with PDF & Quiz Support")

# ✅ PDF Processing
def extract_text_from_pdf(uploaded_file):
    """Extracts text from PDF."""
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

uploaded_pdf = st.file_uploader("📂 Upload a PDF for AI Explanation", type=["pdf"])

if uploaded_pdf:
    st.session_state["pdf_text"] = extract_text_from_pdf(uploaded_pdf)
    st.success(f"📄 PDF '{uploaded_pdf.name}' uploaded successfully!")

# ✅ AI Explanation Function
def get_ai_explanation(user_input, pdf_text=""):
    """Gets an AI-generated explanation."""
    prompt = f"You are an AI tutor. Answer clearly and concisely."
    if pdf_text:
        prompt += f"\nUse the following document as reference:\n{pdf_text[:2000]}"

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content.strip()

# ✅ Chat Interface
st.subheader("💬 Chat with AI Tutor")

# ✅ Display Chat History
for chat in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.write(f"**You:** {chat['question']}")
    with st.chat_message("assistant"):
        st.write(f"**AI Tutor:** {chat['answer']}")

st.write("---")  # ✅ Separator between chat history and input

with st.form("chat_input_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here:")
    submit_chat = st.form_submit_button("Submit")

if submit_chat and user_input:
    ai_response = get_ai_explanation(user_input, st.session_state["pdf_text"])
    st.session_state["chat_history"].append({"question": user_input, "answer": ai_response})
    st.rerun()

# ✅ Quiz System
def extract_json_from_response(response_text):
    """Extracts valid JSON from the AI response and fixes missing brackets."""
    match = re.search(r"\[\s*{.*}\s*\]", response_text, re.DOTALL)
    return match.group(0).strip() if match else None

def generate_quiz(pdf_text):
    """Generates quiz questions in strict JSON format."""
    prompt = (
        f"Generate exactly 5 multiple-choice questions from the following text:\n{pdf_text[:2000]}\n"
        "Return a JSON array in this exact format:\n"
        '[{"question": "What is AI?", "options": ["A) Artificial Intelligence", "B) Machine Learning", "C) Deep Learning", "D) Neural Networks"], "answer": "A) Artificial Intelligence"}]\n'
        "DO NOT include explanations, markdown, or extra text. **Only return the JSON array.**"
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": prompt}]
    )

    response_text = response.choices[0].message.content.strip()

    # ✅ Extract JSON using regex to remove unwanted text
    json_match = re.search(r"\[\s*{.*}\s*\]", response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(0).strip()
    
    # ✅ Try to parse JSON safely
    try:
        quiz_data = json.loads(response_text)
        st.session_state["quiz_questions"] = quiz_data  # ✅ Store quiz questions
        return quiz_data
    except json.JSONDecodeError:
        st.error("❌ AI returned invalid JSON. Please retry.")
        return None


if st.session_state["pdf_text"] and st.button("📝 Start Quiz"):
    st.session_state["quiz_started"] = True
    generate_quiz(st.session_state["pdf_text"])
    st.rerun()

if st.session_state["quiz_started"]:
    st.header("📝 Quiz Time!")

    for idx, q_data in enumerate(st.session_state["quiz_questions"]):
        st.write(f"**Q{idx+1}:** {q_data['question']}")
        st.radio(f"Choose your answer for Q{idx+1}:", q_data["options"], key=f"q{idx+1}")

    if st.button("✅ Submit Quiz"):
        st.session_state["quiz_started"] = False
        st.session_state["quiz_finished"] = True
        st.session_state["score"] = sum(
            1 for idx, q in enumerate(st.session_state["quiz_questions"])
            if st.session_state.get(f"q{idx+1}") == q["answer"]
        )
        st.success(f"✅ Your Score: {st.session_state['score']} / {len(st.session_state['quiz_questions'])}")
        conn = sqlite3.connect("ai_tutor.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quiz_scores (username, score, total_questions) VALUES (?, ?, ?)",
                       (st.session_state["username"], st.session_state["score"], len(st.session_state["quiz_questions"])))
        conn.commit()
        conn.close()
        st.rerun()

if st.session_state["quiz_finished"]:
    st.header("📝 Quiz Finished!")
    st.write(f"✅ Your Score: {st.session_state['score']} / {len(st.session_state['quiz_questions'])}")
    st.write("---")
    st.write("📊 Leaderboard:")
    conn = sqlite3.connect("ai_tutor.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT username, score, total_questions, timestamp FROM quiz_scores ORDER BY score DESC")
    scores = cursor.fetchall()
    conn.close()
    for idx, (username, score, total_questions, timestamp) in enumerate(scores):
        st.write(f"🥇 {username} scored {score} / {total_questions} on {timestamp}")
    st.write("---") 

if st.button("🔄 Restart Quiz"):
    st.session_state["quiz_started"] = False
    st.session_state["quiz_questions"] = []
    st.session_state["quiz_finished"] = False
    generate_quiz(st.session_state["pdf_text"])
    st.rerun()
