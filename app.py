import streamlit as st
from openai import OpenAI

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Configure client to use OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],  # Store your key in .streamlit/secrets.toml
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # OpenRouter requires the provider prefix
        messages=st.session_state.messages,
        extra_headers={  # Recommended by OpenRouter
            "HTTP-Referer": "your-app-url",  # Optional but good practice
            "X-Title": "My Chatbot",         # Optional
        }
    )
    
    bot_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})