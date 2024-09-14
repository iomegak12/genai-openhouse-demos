import os
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI


def main():
    load_dotenv()

    st.set_page_config(
        page_title="CSV Document - Chatbot",
        page_icon=":books:"
    )

    st.title("HR - Attrition Analysis Chatbot")
    st.subheader("Helps to uncover the insights from HR Attrition Data!")

    st.markdown("""
        This chatbot is created to demonstrate how CSV Agents work in Langchain, to showcase
        a business use case of HR Attrition Data Analytics!"
                """)

    user_question = st.text_input(
        "Ask your questions about HR Attrition Data!"
    )

    csv_path = "./hr-employees-attritions-internet.csv"

    llm = ChatOpenAI(
        model = "gpt-4",
        temperature=0,
        max_tokens = 1000,
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )

    df = pd.read_csv(csv_path)

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True
    )

    agent.handle_parsing_errors = True

    answer = agent.invoke(user_question)

    st.write(answer["output"])


if __name__ == "__main__":
    main()
