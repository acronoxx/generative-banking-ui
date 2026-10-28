import os

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model=os.environ["OPENAI_MODEL"],
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
    default_query={"subscription-key": os.environ["OPENAI_API_KEY"]},
)
