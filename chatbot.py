import streamlit as st
from groq import Groq

# Initialize Groq client with API key from secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Streamlit page configuration
st.set_page_config(page_title="Groq AI Chatbot", page_icon="🤖", layout="centered")

# Title
st.title("Groq AI Chatbot")

# Model selection dropdown
model = st.selectbox(
    "Choose a model",
    ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"],
    index=0
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your message?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response with streaming
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant created by xAI."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True
            )
            # Stream response
            response = st.write_stream(chunk.choices[0].delta.content or "" for chunk in stream if chunk.choices[0].delta.content)
            # Save response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {str(e)}")
