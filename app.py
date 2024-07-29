import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the model
model = genai.GenerativeModel('gemini-pro')

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# Custom CSS to style the app
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #0066cc;
        color: white;
    }
    .feedback-button {
        padding: 5px 10px;
        margin: 0 5px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .feedback-button:hover {
        opacity: 0.8;
    }
    .positive {
        background-color: #4CAF50;
        color: white;
    }
    .negative {
        background-color: #f44336;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit app
st.title("Sentient Assistant")

# Sidebar for user options
st.sidebar.title("Options")

# Quick replies
quick_replies = ["Tell me a joke", "What's the weather like?", "Recommend a book", "How does AI work?"]
selected_reply = st.sidebar.selectbox("Quick Replies", ["Select a quick reply"] + quick_replies)

# User feedback function
def get_feedback(message_index):
    col1, col2 = st.columns(2)
    if col1.button("👍", key=f"positive_{message_index}"):
        st.session_state.feedback.append(("positive", message_index))
        st.success("Thank you for your positive feedback!")
    if col2.button("👎", key=f"negative_{message_index}"):
        st.session_state.feedback.append(("negative", message_index))
        st.error("We're sorry to hear that. We'll work on improving.")

# Chat interface
st.subheader("Chat")

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            get_feedback(i)

# User input
user_input = st.chat_input("Type your message here...")

if user_input or (selected_reply != "Select a quick reply"):
    if selected_reply != "Select a quick reply":
        user_input = selected_reply

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate AI response
    response = model.generate_content(user_input)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response.text)
        get_feedback(len(st.session_state.messages) - 1)

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun()

# Display feedback summary
st.sidebar.title("Feedback Summary")
positive_count = sum(1 for feedback in st.session_state.feedback if feedback[0] == "positive")
negative_count = sum(1 for feedback in st.session_state.feedback if feedback[0] == "negative")
st.sidebar.write(f"Positive feedback: {positive_count}")
st.sidebar.write(f"Negative feedback: {negative_count}")

# Footer
st.markdown(
    """
    <div style="position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f0f2f6; text-align: center; padding: 10px; font-size: 14px;">
        Powered by Gemini AI | © 2024 AI Assistant
    </div>
    """,
    unsafe_allow_html=True
)