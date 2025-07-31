from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary :str 
    Soruces: list[str]
    tools_used : list[str]

llm = ChatGroq( model="llama3-8b-8192")

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

