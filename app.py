import streamlit as st
from openai import OpenAI

st.title("Chatbot")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the OpenAI Client
client = OpenAI()

# Display past chat messages from history on app rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Say something..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Request response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    
    # Parse out the bot's reply text
    bot_reply = response.choices[0].message.content

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})