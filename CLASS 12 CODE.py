import os
import streamlit as st
import google.generativeai as genai 

#INITIALIZING SESSION STATE VARIABLES
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

#LOAD API KEY
if os.path.exists(".env"):
 #while running locally import variable from .env
 from dotenv import load_dotenv
 load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    #While running on streamlit, load API key from streamlit secrets
    try:
        API_KEY = st.secrets["API_KEY"]
    except Exception:
        API_KEY : None
if not API_KEY: 
    #If no API Key is found stop the app
    st.error("No API Key Found!")
    st.stop()

#INITIALIZE GENERATIVE AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat(history=[])

#STREAMLIT UI
st.sidebar.title("Chatbot")
st.sidebar.write("Hello, how can I help you")
request = st.sidebar.text_input("Your Message:")
if (request):
    st.session_state.chat_started = True

if (st.session_state.chat_started):
    response = "Something went wrong!"
    try:
        api_response = chat.send_message(request)
        response = api_response.text
        pair = {'request' : request, 'response' : response}
        st.session_state.history.append(pair)

    except Exception as e:
        st.error(f"Error: {e}")
    for pair in st.session_state.history:
        st.info(pair['request'])      #To show prompts in different colors
        st.write(pair['response'])    #to support markdowns