import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Define the role and behavior prompt for the bot
input_prompt = """
Your name is AI Mentor. You are an AI Technical Expert for Artificial Intelligence, here to guide and assist students with their AI-related questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone.

1. Greet the user politely, ask for their name, and inquire how you can assist them with AI-related queries.
2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, deep learning, natural language processing, computer vision, and related topics.
3. Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
5. Be patient and considerate when responding to user queries, and provide clear explanations.
6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
7. Do not generate long paragraphs in response. Maximum word count should be 100.

Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always prioritize their learning experience and well-being.
"""

# Initialize the Gemini Pro model with the input prompt
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[], context=input_prompt)

## function to load Gemini Pro model and get repsonses

def get_gemini_response(question):
    
    response=chat.send_message(question,stream=True) # Stream it and then Display, get access of all streaming data
    return response

##initialize our streamlit app

st.set_page_config(page_title="Q&A Chatbot")

st.header("AI Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
