import os
import groq
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY! Please set it in .env.")

# ✅ Initialize AI client
client = groq.Client(api_key=GROQ_API_KEY)

def get_ai_explanation(user_input, pdf_text=""):
    """Generates an AI response using the GROQ API."""
    
    prompt = "You are an AI tutor. Answer clearly and concisely."
    
    if pdf_text:
        prompt += f"\nUse the following document as reference:\n{pdf_text[:2000]}"
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )
    
    return response.choices[0].message.content.strip()

# ✅ Test the AI response
def get_response(user_input, context=""):
    """Generates an AI response based on user input and optional context (like a PDF)."""
    
    prompt = "You are an AI tutor. Answer clearly and concisely."
    if context:
        prompt += f"\nUse the following reference:\n{context[:2000]}"

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()

def get_quiz_questions(pdf_text):
    """Fetches quiz questions from AI and ensures valid JSON format."""
    prompt = (
        f"Generate exactly 5 multiple-choice questions from the following text:\n{pdf_text[:2000]}\n"
        "Return a JSON array strictly in this format:\n"
        '[{"question": "What is AI?", "options": ["A) Artificial Intelligence", "B) Machine Learning", "C) Deep Learning", "D) Neural Networks"], "answer": "A) Artificial Intelligence"}]\n'
        "DO NOT add explanations, markdown, or extra text. Only return valid JSON."
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
