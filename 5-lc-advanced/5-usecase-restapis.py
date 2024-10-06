import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import APIChain


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

        api_documentation = """
        
        BASE URL: https://restcountries.com/
        
        API Documentation:
        
        The API Endpoint /v3.1/name/{name} Used to get details about a country. All URL parameters are listed below.
        
          - name: Name of the Country - Ex: India, France, Italy
        
        The API Endpoint /v3.1/get-company/{stock-ticker} Used to get company executive details based on stock ticker symbol. All URL Parameters are listed below.
        
          - stock-ticker: 4 letters Stock Ticker Symbol. Examples: APPL, TSLA, NVDA
        
        """

        chain = APIChain.from_llm_and_api_docs(
            llm,
            api_documentation,
            verbose=True,
            limit_to_domains=None
        )
        
        question = "Can you tell me information about France?"
        
        response = chain.invoke(question)
        
        print(response)
        
        question = "Can you tell me about the currency COP?"
        
        response = chain.invoke(question)
        
        print(response)
        
    except Exception as error:
        print(f"Error Occurred, Details : {error}")


if __name__ == "__main__":
    main()
