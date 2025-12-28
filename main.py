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

# Research depth configurations
DEPTH_CONFIGS = {
    "quick": {
        "description": "brief 2-3 sentence summary highlighting only the main points",
        "word_limit": 80
    },
    "detailed": {
        "description": "detailed 4-6 sentence explanation including context and examples",
        "word_limit": 200
    },
    "academic": {
        "description": "6-10 sentence formal, academic-style summary, including citations to sources",
        "word_limit": 400
    }
}

def get_system_message(depth="detailed"):
    """Generate system message based on research depth."""
    config = DEPTH_CONFIGS.get(depth, DEPTH_CONFIGS["detailed"])
    
    return f"""
You are an AI Research Assistant.

Your task:
1. Answer the user's question using **multiple sources**:
   - Use the Wikipedia tool for factual grounding
   - Use the Web Search tool for verification and current information
2. Compare information from both sources:
   - If facts match → confidence_score: 0.9-1.0 (HIGH)
   - If partially match → confidence_score: 0.5-0.8 (MEDIUM)
   - If conflicting → confidence_score: 0.1-0.4 (LOW)
3. Research Depth: {depth.upper()}
   - Provide a {config['description']}
   - Target length: ~{config['word_limit']} words
4. Always include tools_used and sources
5. Only include facts supported by at least one source
6. Be concise, clear, and structured

IMPORTANT: You are a ReAct agent. You must think step-by-step.
When you have gathered enough information, you MUST output a "Final Answer".
The "Final Answer" MUST be a valid JSON object strictly following this format:
{{format_instructions}}

Do not output the JSON schema definitions in your final answer. Only output the instance data.
Do not add "Note:" or reflections after the JSON.
"""

tools = [search_tool, wiki_tool, save_tool]

# Custom handle_parsing_errors function
def handle_parsing_error(error):
    """Fallback logic when the agent fails to parse the output."""
    # Often the agent output is actually the Final Answer stuck in an Action block or malformed
    response_str = str(error)
    # Check if we can extract JSON from the error message itself if it contains the output
    if "Could not parse LLM output" in response_str:
        # The output is usually contained in the error message
        return response_str
    return "Agent encountered a parsing error. Please try again."

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True,
    handle_parsing_errors=True, # LangChain's default handler tries to recover
    max_iterations=5,
    early_stopping_method="generate"
)

def extract_json_from_response(text):
    """Try to extract JSON from various response formats."""
    # Clean up the text
    text = text.replace("```json", "").replace("```", "").strip()
    
    # Strategy 1: Look for the specific JSON structure we expect (ignoring schema)
    # matching {"topic": ...}
    
    try:
        # Find the last occurrence of "topic" to avoid picking up the schema definition
        # if the schema is printed first.
        # But a safer way is to use regex looks for values
        
        # Regex to find a JSON object containing "topic" and "summary"
        # We use a non-greedy match for content
        pattern = r'\{[^{}]*"topic"[^{}]*"summary"[^{}]*\}'
        
        # Search for all matches
        matches = list(re.finditer(pattern, text, re.DOTALL))
        
        if matches:
            # If multiple matches, the last one is likely the result, as schema usually comes first if echoed
            # But let's check which one is valid
            for match in reversed(matches):
                try:
                    candidate = match.group()
                    data = json.loads(candidate)
                    if "topic" in data and "confidence_score" in data:
                        return data
                except:
                    continue
    except:
        pass
        
    # Strategy 2: Brute force JSON extraction
    try:
        # Find start and end braces
        start_indices = [i for i, char in enumerate(text) if char == '{']
        end_indices = [i for i, char in enumerate(text) if char == '}']
        
        if start_indices and end_indices:
            # Try to match the outermost reasonable braces
            # Usually the answer is at the end
            last_end = end_indices[-1]
            
            # Try from the last start brace backwards
            for start in reversed(start_indices):
                if start < last_end:
                    candidate = text[start : last_end + 1]
                    try:
                        data = json.loads(candidate)
                        # Filter out schema definitions (they usually have "properties" or "type")
                        if "properties" not in data and "topic" in data:
                            return data
                    except:
                        continue
    except:
        pass

    return None

def run_agent(query, depth="detailed"):
    """Run the research agent with specified depth and return structured response."""
    try:
        system_message = get_system_message(depth)
        # We need to give the format instructions clearly
        format_instructions = parser.get_format_instructions()
        formatted_query = system_message.format(format_instructions=format_instructions) + f"\nUser Query: {query}"
        
        print(f"[DEBUG] Running agent with query: {query}, depth: {depth}")
        
        # Run the agent
        # Because handle_parsing_errors=True, this should return a string even if parsing fails
        raw_response = agent.run(formatted_query)
        
        print(f"[DEBUG] Raw response: {raw_response[:500]}...")
        
        # Clean up the response if it includes "Final Answer:" prefix from the agent output
        if "Final Answer:" in raw_response:
            raw_response = raw_response.split("Final Answer:", 1)[1].strip()

        # Try to parse with Pydantic first (cleanest)
        try:
            structured_response = parser.parse(raw_response)
            return {"result": structured_response.model_dump()}
        except Exception:
            # Fallback extraction
            print("[DEBUG] Pydantic parse failed, attempting manual extraction...")
            extracted = extract_json_from_response(raw_response)
            if extracted:
                return {"result": extracted}
            
            # Create graceful fallback
            print("[DEBUG] Manual extraction failed, creating fallback response")
            return {
                "result": {
                    "topic": query,
                    "summary": f"Research completed but output format was irregular. Raw output summary: {raw_response[:200]}...",
                    "sources": ["Agent Output"],
                    "tools_used": ["search"],
                    "confidence_score": 0.5
                }
            }
            
    except Exception as e:
        print(f"[ERROR] Agent error: {str(e)}")
        # Check if it's a Groq deprecation error specifically
        if "model `llama3-8b-8192` has been decommissioned" in str(e):
             return {
                "error": "Model deprecated. Please notify administrator to update the model in main.py.",
                "raw_response": str(e)
            }
            
        return {
            "error": "An error occurred during research.", 
            "raw_response": str(e)
        }