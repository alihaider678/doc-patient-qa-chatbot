import streamlit as st
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Load transcript data
with open("transcript_data.json") as f:
    transcript_data = json.load(f)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

## function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    prompt = f"Based on the following transcript data: {json.dumps(transcript_data)}\n\nQuestion: {question}\nAnswer:"
    response = chat.send_message(prompt, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    return response_text

# Streamlit application
st.set_page_config(page_title="Doctor-Patient Chatbot", page_icon=":hospital:")

st.markdown("""
    <style>
    .main {
        background-color: #ffffff 
;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .chatbox {
        background-color: #ffffff;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 10px;
        max-width: 700px;
        margin: 10px 0;
    }
    .chatbox .user {
        text-align: right;
        color: #007bff;
    }
    .chatbox .bot {
        text-align: left;
        color: #28a745;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Doctor-Patient Chatbot :hospital:")
st.write("This chatbot allows you to ask questions based on the doctor-patient transcript.")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input
input_text = st.text_input("Ask a question about the transcript:", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text)
    st.session_state['chat_history'].append(("You", input_text))
    st.session_state['chat_history'].append(("Bot", response))

# Display chat history
for role, text in st.session_state['chat_history']:
    align = 'user' if role == 'You' else 'bot'
    st.markdown(f'<div class="chatbox {align}">{role}: {text}</div>', unsafe_allow_html=True)