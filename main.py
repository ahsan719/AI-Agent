from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

load_dotenv()

llm =ChatOpenAI(model="gpt-3.5-turbo")
