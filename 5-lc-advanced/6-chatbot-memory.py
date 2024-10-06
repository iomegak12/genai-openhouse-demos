import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


def main():
    try:
        load_dotenv()

        model_name = "gpt-4"
        openai_api_key = os.environ["OPENAI_API_KEY"]

        llm = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            max_tokens=1000,
            openai_api_key=openai_api_key
        )

        template = """
            You're a chatbot that is helpful.
            Your goal is to help the user, but also make jokes.
            Take what the user is saying and make a joke out of it along with the correct answer.
            
            {chat_history}
            
            Human: {human_input}
            
            Chatbot:
        """

        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"],
            template=template
        )

        memory = ConversationBufferMemory(memory_key="chat_history")

        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory
        )

        response = llm_chain.predict(
            human_input="Is a pear a fruit or a vegetable")

        print(response)

        response = llm_chain.predict(
            human_input="What was one of the fruits i asked about earlier?")

        print(response)
    except Exception as error:
        print(f"Error Occurred, Details : {error}")


if __name__ == "__main__":
    main()
