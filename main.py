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

# Strict length enforcement configurations
DEPTH_CONFIGS = {
    "quick": {
        "description": "Ultra-concise summary. Maximum 3 sentences.",
        "word_limit": "50-80"
    },
    "detailed": {
        "description": "Comprehensive explanation with context. 2-3 paragraphs.",
        "word_limit": "200-300"
    },
    "academic": {
        "description": "In-depth formal analysis with citations. 4-5 paragraphs.",
        "word_limit": "400-600"
    }
}

def get_system_message(depth="detailed"):
    config = DEPTH_CONFIGS.get(depth, DEPTH_CONFIGS["detailed"])
    
    return f"""
You are an AI Research Assistant. Your goal is to answer the user's query with high accuracy and strict adherence to length constraints.

### RESEARCH PROTOCOL:
1. **Search**: Use `search` or `wikipedia` to gather facts.
2. **Verify**: Cross-reference at least two sources.
3. **Synthesize**: Create a final answer based on the {depth.upper()} depth.

### STRICT OUTPUT REQUIREMENTS:
- **Depth**: {depth.upper()} ({config['description']})
- **Length**: MUST be between {config['word_limit']} words. Do NOT generate less or more.
- **Format**: Return ONLY a valid JSON object. No markdown, no "Final Answer:" prefix, no "Thought:" trace in the final output.

### JSON STRUCTURE:
{{format_instructions}}

### CRITICAL RULES:
- If you have enough info, STOP searching and output the JSON immediately.
- Do NOT output the schema or explanations.
- The `summary` field MUST meet the word count requirement of {config['word_limit']} words.
"""

tools = [search_tool, wiki_tool, save_tool]

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=4, # Reduced to prevent loops
    early_stopping_method="generate"
)

def clean_json_text(text):
    """Clean text to isolate the JSON part."""
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    if start_idx != -1 and end_idx != -1:
         return text[start_idx : end_idx + 1]
    return text

def extract_json_from_response(text):
    """Robustly extract JSON from text."""
    cleaned_text = clean_json_text(text)
    try:
        return json.loads(cleaned_text)
    except:
        pass
        
    # Regex fallback
    try:
        topic_match = re.search(r'"topic":\s*"([^"]+)"', text)
        summary_match = re.search(r'"summary":\s*"([^"]+)"', text)
        if topic_match and summary_match:
             return {
                "topic": topic_match.group(1),
                "summary": summary_match.group(1),
                "sources": ["Extracted"],
                "tools_used": ["search"],
                "confidence_score": 0.5
            }
    except:
        pass
    return None

def run_agent(query, depth="detailed"):
    try:
        system_message = get_system_message(depth)
        formatted_query = system_message.format(format_instructions=parser.get_format_instructions()) + f"\nUser Query: {query}"
        
        print(f"[DEBUG] Running agent with query: {query} | Depth: {depth}")
        raw_response = agent.run(formatted_query)
        
        # Clean response
        if "Final Answer:" in raw_response:
            raw_response = raw_response.split("Final Answer:", 1)[1].strip()
        
        raw_response = clean_json_text(raw_response)

        try:
            structured_response = parser.parse(raw_response)
            return {"result": structured_response.model_dump()}
        except:
            extracted = extract_json_from_response(raw_response)
            if extracted:
                return {"result": extracted}
            
            # Fallback
            return {
                "result": {
                    "topic": query,
                    "summary": f"Could not parse valid JSON. Raw output: {raw_response[:200]}...",
                    "sources": ["System"],
                    "tools_used": ["search"],
                    "confidence_score": 0.0
                }
            }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": str(e), "raw_response": str(e)}