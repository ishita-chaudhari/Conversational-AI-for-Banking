import streamlit as st
from agent import agent
from tools.detect_fraud import classify_fraud_in_input  

st.set_page_config(page_title="Bank AI Chatbot", layout="centered")
st.title("🏦 Bank Conversational AI")

# Conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
user_input = st.chat_input("How can I assist you today?")

if user_input:
    
    suspicious = classify_fraud_in_input(user_input)
    if suspicious:
        st.session_state.history.append(("User", user_input))
        st.session_state.history.append(("BankBot", suspicious))
    else:
        with st.spinner("Processing..."):
            response = agent.run(user_input)
            st.session_state.history.append(("User", user_input))
            st.session_state.history.append(("BankBot", response))

# Display chat history
for speaker, message in st.session_state.history:
    if speaker == "User":
        with st.chat_message("User"):
            st.markdown(message)
    else:
        with st.chat_message("Assistant"):
            st.markdown(message)
