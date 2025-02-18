import streamlit as st
import json
import os

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

def show_login():
    """Login & Signup System"""
    st.sidebar.title("🔐 User Authentication")

    users = load_users()
    
    tab1, tab2 = st.sidebar.tabs(["Login", "Signup"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if username in users and users[username]["password"] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.sidebar.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid Username or Password")

    with tab2:
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        if st.button("Signup"):
            if new_username in users:
                st.sidebar.error("❌ Username already exists!")
            else:
                users[new_username] = {"password": new_password}
                save_users(users)
                st.sidebar.success("✅ Account created! Please log in.")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    show_login()
    st.stop()

def show_signup():
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
