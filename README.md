# 🧠 AI Tutor with RAG and Adaptive Learning  

An AI-powered tutoring system with **Retrieval-Augmented Generation (RAG)**, **adaptive quizzes**, and **performance tracking** to personalize student learning.

## 🚀 Features  

✅ **Retrieval-Augmented Generation (RAG)** – Uses vector databases for accurate AI responses  
✅ **AI Chatbot** – Provides subject-specific explanations  
✅ **Quiz Generation** – Creates dynamic quizzes from PDFs  
✅ **Adaptive Learning System** – Adjusts quiz difficulty based on performance  
✅ **Student Performance Dashboard** – Tracks progress and suggests resources  
✅ **SQLite Database** – Stores quiz attempts and student progress  
✅ **Streamlit UI** – Simple and interactive frontend  

---

## 📂 Project Structure  

```
📦 AI-Tutor  
│── 📂 data/                 # PDFs & knowledge base  
│── 📂 assets/               # Logos, icons, and images  
│── 📂 models/               # Vector database and LLM models  
│── 📂 env/                  # Environment files  
│── 📂 logs/                 # System logs  
│── app.py                   # Main Streamlit app  
│── login.py                 # User authentication  
│── chat.py                  # AI Chatbot logic  
│── quiz.py                  # Quiz generation  
│── dashboard.py             # Performance tracking  
│── database.py              # SQLite operations  
│── utils.py                 # Helper functions  
│── styles.css               # UI customization  
│── README.md                # Project documentation  
│── requirements.txt         # Python dependencies  
│── .gitignore               # Ignored files  
```
## 🏗️ Installation  

### 1️⃣ Clone the repository  
```sh
git clone https://github.com/saiteja-muthyala/AI-Tutor.git
cd AI-Tutor
```

### 2️⃣ Create a virtual environment  
```sh
python -m venv ai_tutor_env  
source ai_tutor_env/bin/activate  # Mac/Linux  
ai_tutor_env\Scripts\activate     # Windows  
```

### 3️⃣ Install dependencies  
```sh
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables  
Create a `.env` file in the root directory and add:  
```sh
OPENAI_API_KEY=your_openai_api_key
CHROMADB_PATH=data/vector_db
```

---

## 🚀 Running the Application  

Start the AI Tutor using:  
```sh
streamlit run app.py
```

Then, open [localhost:8501](http://localhost:8501/) in your browser.

---

## 🔍 Implemented RAG (Retrieval-Augmented Generation)  

### ✅ **1. Document Ingestion**
Extracts content from **PDFs, textbooks, and notes** for knowledge retrieval.  

### ✅ **2. Vector Database**
Uses **FAISS / ChromaDB / Pinecone** to store and retrieve relevant data.  

### ✅ **3. Context-Aware Responses**
AI generates **accurate answers** based on retrieved content.  

### ✅ **4. Quiz Generation**
Creates **personalized questions** using retrieved knowledge.  

---

## 📢 Deployment on GitHub & Streamlit Cloud  

### **1️⃣ Push Code to GitHub**  
```sh
git add .  
git commit -m "Initial commit"  
git push origin main  
```

### **2️⃣ Deploy on Streamlit Cloud**  
1. Go to [Streamlit Cloud](https://share.streamlit.io/)  
2. Connect your GitHub repository  
3. Set `app.py` as the **main file**  
4. Deploy 🎉  


## 📚 Future Enhancements  
- ✅ **Speech-to-Text Support** 🎤  
- ✅ **More LLM Models (Llama 2, GPT-4 Turbo, Mistral)** 🤖  
- ✅ **Multi-User Progress Tracking** 📊  


## 💡 Contributions  
Want to improve this project? **Fork it, modify it, and submit a pull request!**  

## 🎯 License  
This project is **MIT Licensed** – Feel free to use and modify!  
