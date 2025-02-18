import streamlit as st
import json
import re
import database 
import ai 
import groq  

# ✅ Load API key from Streamlit secrets
client = groq.Client(api_key=st.secrets["GROQ_API_KEY"])

# ✅ Ensure all required session state variables are initialized
for key, default in {
    "quiz_questions": [],
    "quiz_started": False,
    "quiz_finished": False,
    "score": 0,
    "user_answers": {},
    "pdf_text": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def extract_json_from_response(response_text):
    """Extract JSON from AI response and fix formatting issues."""
    match = re.search(r"\[\s*{.*}\s*\]", response_text, re.DOTALL)
    return match.group(0).strip() if match else None

def generate_quiz():
    """Generate quiz questions from AI and store them in session state."""
    if "pdf_text" not in st.session_state or not st.session_state["pdf_text"]:
        st.error("❌ No PDF text found. Please upload a PDF first.")
        return
    
    st.session_state["quiz_questions"] = []  # Clear previous quiz
    st.session_state["quiz_started"] = False
    
    st.info("🔄 Fetching quiz questions from AI...")

    response_text = ai.get_quiz_questions(st.session_state["pdf_text"])  # AI call

    # 🔍 Debug: Check Raw AI Response
    st.session_state["raw_ai_response"] = response_text  

    response_text = extract_json_from_response(response_text)

    if response_text:
        try:
            quiz_data = json.loads(response_text)  # ✅ Parse JSON safely
            if isinstance(quiz_data, list):  # Ensure it's a list
                st.session_state["quiz_questions"] = quiz_data
                st.session_state["quiz_started"] = True
                st.success("✅ Quiz questions generated!")
                st.rerun()
            else:
                st.error("❌ AI response was not in expected list format.")
        except json.JSONDecodeError:
            st.error("❌ AI returned invalid JSON. Please retry.")
    else:
        st.error("❌ AI response did not contain valid JSON!")

def quiz_ui():
    """Handles the quiz UI and user interactions."""
    st.header("📝 Quiz Section")

    # ✅ Ensure session state variables are initialized
    if "quiz_questions" not in st.session_state:
        st.session_state["quiz_questions"] = []

    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = {}

    if "quiz_started" not in st.session_state:
        st.session_state["quiz_started"] = False

    if "quiz_submitted" not in st.session_state:
        st.session_state["quiz_submitted"] = False

    # ✅ Start Quiz Button
    if not st.session_state["quiz_started"]:
        if st.button("📝 Start Quiz"):
            st.session_state["quiz_started"] = True  # Mark quiz as started
            generate_quiz()  # Generate new quiz
            st.rerun()  # Refresh UI to show questions

    # ✅ If quiz hasn't started, show message
    if not st.session_state["quiz_started"]:
        st.warning("⚠️ Click 'Start Quiz' to begin!")
        return

    # ✅ Ensure quiz questions are available
    if not st.session_state["quiz_questions"]:
        st.error("❌ No quiz questions available. Please try again.")
        return

    score = 0  # Track user score

    # ✅ Display quiz questions
    for idx, q_data in enumerate(st.session_state["quiz_questions"]):
        q_text = q_data.get("question", "No question found.")
        options = q_data.get("options", ["Option A", "Option B", "Option C", "Option D"])
        correct_answer = q_data.get("answer", "")

        # ✅ Display each question with options
        st.write(f"**Q{idx + 1}: {q_text}**")
        user_choice = st.radio(f"Choose your answer for Q{idx+1}:", options, key=f"q{idx+1}")

        # ✅ Store user answer
        st.session_state["user_answers"][f"q{idx+1}"] = user_choice

        # ✅ Show correct/incorrect answer after submission
        if st.session_state["quiz_submitted"]:
            if user_choice == correct_answer:
                st.success(f"✅ Correct! The answer is **{correct_answer}**")
                score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer is **{correct_answer}**")

    # ✅ Submit Quiz Button
    if st.button("✅ Submit Quiz"):
        st.session_state["quiz_submitted"] = True
        st.rerun()  # Refresh UI to display correct/incorrect answers

    # ✅ Display final score after submission
    if st.session_state["quiz_submitted"]:
        total_questions = len(st.session_state["quiz_questions"])
        st.success(f"🏆 Your Score: **{score} / {total_questions}**")


def get_quiz_questions(pdf_text):
    """Calls AI to generate quiz questions from the given text."""
    prompt = (
        f"Generate exactly 5 multiple-choice questions from this text:\n{pdf_text[:2000]}\n"
        "Return a JSON array in this format:\n"
        '[{"question": "What is AI?", "options": ["A) Artificial Intelligence", "B) Machine Learning", "C) Deep Learning", "D) Neural Networks"], "answer": "A) Artificial Intelligence"}]\n'
        "DO NOT include explanations, markdown, or extra text. Return JSON only."
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": prompt}]
    )

    response_text = response.choices[0].message.content.strip()
    print("🔍 [DEBUG] AI Raw Response:", response_text)  # Debugging AI Response

    return response_text  # Return raw response for debugging

def submit_quiz():
    """Handles quiz submission and scoring."""
    if not st.session_state["quiz_questions"]:
        st.error("❌ No quiz available. Start a new quiz first.")
        return

    st.session_state["score"] = sum(
        1 for idx, q in enumerate(st.session_state["quiz_questions"])
        if st.session_state.get(f"q{idx+1}") == q["answer"]
    )

    database.save_quiz_score(
        st.session_state.get("username", "Guest"),
        st.session_state["score"],
        len(st.session_state["quiz_questions"])
    )

    st.success(f"✅ Your Score: {st.session_state['score']} / {len(st.session_state['quiz_questions'])}")

# 🔄 Restart Quiz Button
if st.button("🔄 Restart Quiz"):
    st.session_state["quiz_started"] = False
    st.session_state["quiz_questions"] = []
    st.session_state["quiz_finished"] = False
    st.session_state["user_answers"] = {}
    st.session_state["score"] = 0

    # ✅ Regenerate quiz questions
    generate_quiz()

    # ✅ Refresh the UI
    st.rerun()
