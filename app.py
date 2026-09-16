import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful assistant.")
    ]

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

user_input = st.chat_input("Write your question")

if user_input:
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    st.chat_message("user").write(user_input)

    response = llm.invoke(st.session_state.chat_history)

    if isinstance(response.content, str):
        answer = response.content
    else:
        answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict)
        )

    st.session_state.chat_history.append(
        AIMessage(content=answer)
    )

    st.chat_message("assistant").write(answer)
