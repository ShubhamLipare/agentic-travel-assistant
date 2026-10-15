
import streamlit as st

from agent import ask_agent

st.set_page_config(
    page_title="Agentic Travel Assistant",
    page_icon="✈️",
)

st.title("✈️ Agentic AI Travel Assistant")
st.caption("Ask about weather or country information.")

question = st.text_input(
    "What would you like to know?",
    placeholder="What's the weather in Pune?",
)

if st.button("Ask assistant", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("The assistant is working..."):
            try:
                answer = ask_agent(question.strip())
                st.markdown(answer)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
