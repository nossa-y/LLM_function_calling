import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from PIL import Image

# Load environment variables from .env (if available)
load_dotenv()

# Main Title and prompt template input
im = Image.open("images/logo.png")
st.set_page_config(
    page_title="Sales Booster",
    page_icon=im,
    layout="wide",
)
st.image(im, width=150)

# Add main title
st.title("Sales Booster")

# Set Streamlit page configuration and custom CSS for chat styling
st.markdown("""
    <style>
        .chat-container { margin: 20px; }
        .user-message { 
            background-color: #dcf8c6; 
            padding: 10px; 
            border-radius: 10px; 
            text-align: right; 
            margin-bottom: 10px;
        }
        .assistant-message { 
            background-color: #f1f0f0; 
            padding: 10px; 
            border-radius: 10px; 
            text-align: left; 
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar: Ask for GPT credentials
st.sidebar.header("Credentials")
gpt_api_key = st.sidebar.text_input("Enter your Anthropic API key:", type="password")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize format counter in session state if not present
if "format_counter" not in st.session_state:
    st.session_state.format_counter = 0

# Display chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'><b>You:</b> {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'><b>Assistant:</b> {message['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input area for user's message
user_message = st.text_input("Your message:")

# When the user clicks Send...
if st.button("Send") and user_message:
    # Save the user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    if gpt_api_key:
        os.environ["OPENAI_API_KEY"] = gpt_api_key
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        
        # Different system messages based on the message count
        if st.session_state.format_counter == 0:
            system_message = """You are a helpful sales AI agent. Format your response exactly as follows:

1. Potential Prospects:
   Here is some potentials prospects I found scraping the web: file saved in directory as clients.csv

2. Personalized Emails:
   I developed personalised mails ready to be sent for each of them, you can complete the transfer following this link: [link]

3. Social Media Content:
   I created a twitter/linkedin post ready to be posted based on latest AI news: 
   You can complete the posting and scheduling following this link: 
   (https://dev.agentinbox.ai/?agent_inbox=901c97ac-806f-4726-b37d-0809a6daab92&inbox=interrupted&limit=10&offset=0&view_state_thread_id=2dc04075-a5a4-49de-b6a0-fb17bb20bc86)

4. Phone Caller Agent:
   Phone caller agent ready, you can test it by calling this phone number: +12253250158

Please in the end ask: Which company should the test agent focus on?"""
        # elif st.session_state.format_counter == 1:
        #    system_message = "You are a helpful sales AI agent. Please only answer: Which company should the test agent focus on?"
        else:
            system_message = "You are a helpful sales AI agent. Please respond with 'done!'"

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message)
        ]
        assistant_response = llm(messages).content
        
        # Increment the format counter
        st.session_state.format_counter += 1
    else:
        assistant_response = f"(No API key provided) Echo: {user_message}"
    
    # Save the assistant's response and update the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    
    # Clear the input field
    st.session_state.user_input = ""

    # Rerun the app to refresh the chat display
    st.experimental_rerun()