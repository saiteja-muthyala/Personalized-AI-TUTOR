import streamlit as st
import ai  # Import AI response handler
from utils import extract_text_from_pdf  # Ensure utils functions are correctly imported

# ✅ Ensure all session state variables are initialized
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""

def get_ai_explanation(user_input):
    """Gets an AI-generated explanation using the uploaded PDF content."""
    prompt = "You are an AI tutor. Answer clearly and concisely."

    if st.session_state["pdf_text"]:
        prompt += f"\nUse this document as reference:\n{st.session_state['pdf_text'][:2000]}"

    response = ai.get_response(user_input, prompt)
    return response

def chat_ui():
    """Chat interface for AI tutor."""
    st.title("💬 AI Tutor Chat")

    # ✅ File uploader for PDF
    uploaded_file = st.file_uploader("📂 Upload a PDF", type=["pdf"], key="chat_pdf_1")
    if uploaded_file:
        st.session_state["pdf_text"] = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF uploaded successfully!")

    # ✅ Display chat history only if messages exist
    if st.session_state["chat_history"]:
        st.subheader("📝 Chat History:")
        for chat in st.session_state["chat_history"]:
            with st.chat_message("user"):
                st.write(f"**You:** {chat['question']}")
            with st.chat_message("assistant"):
                st.write(f"**AI Tutor:** {chat['answer']}")

    st.write("---")  # ✅ Separator

    # ✅ User input field
    user_input = st.text_input("Ask your question:")

    if st.button("Send"):
        if user_input.strip():
            ai_response = get_ai_explanation(user_input)

            # ✅ Store conversation history
            st.session_state["chat_history"].append({"question": user_input, "answer": ai_response})

            # ✅ Display AI response
            with st.chat_message("assistant"):
                st.write(ai_response)

            # ✅ Refresh UI to display the message
            st.rerun()
