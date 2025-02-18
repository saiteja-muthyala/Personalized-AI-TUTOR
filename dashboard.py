import streamlit as st
import database
import pandas as pd
import matplotlib.pyplot as plt

def categorize_skill(avg_score):
    """Categorizes user skill level based on average score."""
    if avg_score >= 80:
        return "🌟 Advanced"
    elif avg_score >= 50:
        return "📘 Intermediate"
    else:
        return "🔰 Beginner"

study_materials = {
    "mathematics": ["📖 Algebra Essentials", "🎥 Calculus for Beginners", "🔗 Khan Academy - Advanced Math"],
    "java": ["📖 Java OOP Concepts", "🎥 Effective Java Programming", "🔗 Java Tutorials (GeeksforGeeks)"],
    "python": ["📖 Python Crash Course", "🎥 Data Science with Python", "🔗 Python OOP Principles"],
    "c": ["📖 C Programming Absolute Beginner's Guide", "🎥 C Programming in One Video", "🔗 Learn-C.org - Free C Tutorials"],
    "c++": ["📖 The C++ Programming Language by Bjarne Stroustrup", "🎥 C++ STL Masterclass", "🔗 Cplusplus.com - C++ Reference"],
    "physics": ["📖 Fundamentals of Physics", "🎥 Quantum Mechanics Explained", "🔗 MIT OpenCourseWare - Physics"],
    "chemistry": ["📖 Organic Chemistry Basics", "🎥 Chemical Reactions Explained", "🔗 Coursera - Chemistry Essentials"],
    "ai": ["📖 Deep Learning with Python", "🎥 AI Ethics and Bias", "🔗 Stanford AI Course"]
}

def get_study_recommendations(username):
    """Recommends study materials based on quiz topic and student performance."""

    # ✅ Get the last quiz topic
    last_topic = st.session_state.get("quiz_topic", "General Knowledge")  

    # ✅ Default study materials based on detected topic
    study_materials = {
        "java": [
            "📖 Java: The Complete Reference - Herbert Schildt",
            "🎥 Java Programming for Beginners (YouTube Series)",
            "📝 Java Design Patterns Cheat Sheet",
        ],
        "python": [
            "📖 Automate the Boring Stuff with Python - Al Sweigart",
            "🎥 Python Crash Course (YouTube Playlist)",
            "📝 Python Data Science Handbook - Jake VanderPlas",
        ],
        "c++": [
            "📖 The C++ Programming Language - Bjarne Stroustrup",
            "🎥 C++ for Beginners (YouTube Series)",
            "📝 C++ STL Quick Reference",
        ],
        "math": [
            "📖 Introduction to Algebra - Art of Problem Solving",
            "🎥 Khan Academy Mathematics Series",
            "📝 Calculus Cheat Sheet",
        ],
        "default": [
            "📖 Learning How to Learn - Barbara Oakley",
            "🎥 Effective Study Habits (YouTube Lecture)",
            "📝 Memory Techniques for Students",
        ],
    }

    # ✅ Select study materials based on last detected topic
    recommended_books = study_materials.get(last_topic.lower(), study_materials["default"])

    # ✅ Display study recommendations
    st.subheader("📚 Recommended Study Materials")
    for book in recommended_books:
        st.write(book)

def recommend_study_materials(score, quiz_topic):
    """Recommends study materials based on the quiz topic and score."""
    if score < 40:
        level = "📕 Beginner"
    elif score < 70:
        level = "📘 Intermediate"
    else:
        level = "📗 Advanced"

    quiz_topic = quiz_topic.lower()
    best_match = next((key for key in study_materials if key in quiz_topic), "general")

    st.write(f"📊 **Your Skill Level: {level} ({score}%)**")
    if best_match in study_materials:
        st.write(f"📚 **Recommended Study Materials for {quiz_topic.title()}**:")
        for item in study_materials[best_match]:
            st.write(item)
    else:
        st.write("❌ No specific recommendations found for this topic.")


def performance_dashboard():
    """Displays student performance insights with analysis and recommendations."""
    st.subheader("📊 Student Performance Insights")

    username = st.session_state.get("username", "Guest")
    past_scores = database.get_user_quiz_history(username)

    if not past_scores:
        st.warning("🔍 No past quiz scores found. Take a quiz to see your progress!")
        return

    # Convert past scores to DataFrame
    df = pd.DataFrame(past_scores, columns=["Score", "Total Questions", "Date"])
    df["Percentage"] = (df["Score"] / df["Total Questions"]) * 100

    # Display past scores
    st.write("📅 Your Last 5 Quiz Scores:")
    st.dataframe(df)

    # **1️⃣ Skill Categorization**
    avg_score = df["Percentage"].mean()
    skill_level = categorize_skill(avg_score)
    st.write(f"📊 **Your Skill Level:** {skill_level} ({avg_score:.2f}%)")

    # **2️⃣ Study Recommendations**
    if avg_score < 50:
        st.warning("❌ You're struggling! Recommended Resources:")
        st.markdown("- 📖 [Introduction to AI](https://www.example.com/ai)")
        st.markdown("- 🎥 [Neural Networks for Beginners](https://www.example.com/neural)")
    elif avg_score < 80:
        st.info("📚 You're improving! Here are some advanced topics:")
        st.markdown("- 📖 [Deep Learning Basics](https://www.example.com/deep-learning)")
        st.markdown("- 🎥 [AI Ethics and Bias](https://www.example.com/ethics)")
    else:
        st.success("🌟 You're Advanced! Try exploring:")
        st.markdown("- 🚀 [Reinforcement Learning](https://www.example.com/rl)")
        st.markdown("- 🤖 [AI Research Papers](https://www.example.com/research)")

    # **3️⃣ Performance Trend Line Chart**
    st.subheader("📈 Your Quiz Performance Trend")
    plt.figure(figsize=(8, 4))
    plt.plot(df["Date"], df["Percentage"], marker="o", linestyle="-", color="blue", label="Your Score")
    plt.xlabel("Date")
    plt.ylabel("Score (%)")
    plt.title("Quiz Performance Over Time")
    plt.xticks(rotation=30)
    plt.legend()
    st.pyplot(plt)

    # **4️⃣ Compare with Class Average**
    class_avg = database.get_class_average_score()
    st.subheader("🏆 Class Performance Comparison")
    st.write(f"📊 **Your Avg Score:** {avg_score:.2f}%")
    st.write(f"📌 **Class Avg Score:** {class_avg:.2f}%")

    if avg_score > class_avg:
        st.success("🚀 You're performing above the class average!")
    else:
        st.warning("📉 Keep practicing to beat the class average!")

    # **5️⃣ Show Incorrect Answers with Explanations**
    st.subheader("❌ Review Incorrect Answers")
    incorrect_questions = database.get_incorrect_answers(username)
    if incorrect_questions:
        for q in incorrect_questions:
            st.write(f"❌ **Question:** {q['question']}")
            st.write(f"📝 **Your Answer:** {q['user_answer']}")
            st.write(f"✅ **Correct Answer:** {q['correct_answer']}")
            st.write(f"📌 **Explanation:** {q['explanation']}")
            st.write("---")
    else:
        st.success("🎯 Great job! You answered all questions correctly.")
