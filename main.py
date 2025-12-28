from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import initialize_agent, AgentType, Tool
from tools import search_tool, wiki_tool, save_tool
import json
import re

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    confidence_score: float

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Enhanced prompt for multi-source research
system_message = """
You are an AI Research Assistant with a rigorous research methodology.

Your task:
1. ALWAYS answer using **multiple sources**:
   - Use the Wikipedia tool for factual grounding
   - Use the Web Search tool for verification and current information
2. Compare information from both sources:
   - If both agree → confidence_score: 0.9-1.0 (HIGH)
   - If partially agree → confidence_score: 0.5-0.8 (MEDIUM)  
   - If conflicting → confidence_score: 0.1-0.4 (LOW)
3. ALWAYS include tools_used and sources in your response
4. ONLY include facts supported by at least one source
5. Be concise, clear, and structured in your summary

Wrap the output in this format and provide no other text:
{format_instructions}
"""

tools = [search_tool, wiki_tool, save_tool]

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,  # Limit iterations to prevent infinite loops
    early_stopping_method="generate"
)

def extract_json_from_response(text):
    """Try to extract JSON from various response formats."""
    # Try to find JSON in the response
    json_patterns = [
        r'\{[^{}]*"topic"[^{}]*\}',  # Simple JSON object
        r'\{.*?"topic".*?"summary".*?"sources".*?"tools_used".*?"confidence_score".*?\}',  # Full structure
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
    
    return None

def run_agent(query):
    """Run the research agent and return structured response."""
    try:
        formatted_query = system_message.format(format_instructions=parser.get_format_instructions()) + f"\nUser Query: {query}"
        
        print(f"[DEBUG] Running agent with query: {query}")
        raw_response = agent.run(formatted_query)
        print(f"[DEBUG] Raw response: {raw_response}")
        
        # Try to parse with Pydantic first
        try:
            structured_response = parser.parse(raw_response)
            return {"result": structured_response.model_dump()}
        except Exception as parse_error:
            print(f"[DEBUG] Pydantic parse failed: {parse_error}")
            
            # Try to extract JSON manually
            extracted = extract_json_from_response(raw_response)
            if extracted:
                return {"result": extracted}
            
            # Fallback: Create a basic response from raw text
            return {
                "result": {
                    "topic": query,
                    "summary": raw_response[:1000] if len(raw_response) > 1000 else raw_response,
                    "sources": ["AI Agent Research"],
                    "tools_used": ["search", "wikipedia"],
                    "confidence_score": 0.5
                }
            }
            
    except Exception as e:
        print(f"[ERROR] Agent error: {str(e)}")
        return {
            "error": str(e), 
            "raw_response": "The agent encountered an error. Please try again."
        }