import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# page config
st.set_page_config(page_title="Sanmi AI Chatbot", page_icon="🤖")
st.title("🤖 Sanmi's AI Chatbot")
st.caption("Built with Groq + Streamlit by Sanmi")

# initialize memory — st.session_state persists across reruns
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Be concise and friendly."
        }
    ]

# display chat history on screen
for msg in st.session_state.messages:
    if msg["role"] != "system":              # don't show system prompt
        with st.chat_message(msg["role"]):   # shows user or bot bubble
            st.markdown(msg["content"])

# chat input box at bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # add to memory
    st.session_state.messages.append({"role": "user", "content": user_input})

    # call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # show bot reply
    with st.chat_message("assistant"):
        st.markdown(reply)

    # add bot reply to memory
    st.session_state.messages.append({"role": "assistant", "content": reply})