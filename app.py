# app.py

import streamlit as st
from dotenv import load_dotenv

# Load environment variables at the very beginning
load_dotenv()

from agent import agent
from tools.detect_fraud import classify_fraud_in_input

st.set_page_config(page_title="Bank AI Chatbot", layout="centered")
st.title("🏦 Bank Conversational AI")

# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
user_input = st.chat_input("How can I assist you today?")

if user_input:
    try:
        suspicious = classify_fraud_in_input(user_input)
    except Exception as e:
        st.error(f"Fraud detection failed: {e}")
        suspicious = None

    if suspicious:
        st.session_state.history.append(("User", user_input))
        st.session_state.history.append(("BankBot", suspicious))
    else:
        with st.spinner("Processing..."):
            try:
                response = agent.run(user_input)
                st.session_state.history.append(("User", user_input))
                st.session_state.history.append(("BankBot", response))
            except Exception as e:
                st.session_state.history.append(("User", user_input))
                st.session_state.history.append(("BankBot", f"❌ Error: {e}"))

# Display chat history
for speaker, message in st.session_state.history:
    with st.chat_message(speaker):
        st.markdown(message)