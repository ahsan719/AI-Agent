from langchain.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from duckduckgo_search import DDGS
from datetime import datetime

# Custom Search Tool using DDGS directly for better stability
def search_func(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if results:
                # Format results string
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
            return "No search results found."
    except Exception as e:
        return f"Search error: {str(e)}"

search_tool = Tool(
    name="search",
    func=search_func,
    description="Search the web for information. Input should be a specific search query.",
)

# Wikipedia Tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# Save Tool
def save_to_txt(data, filename: str = "research_output.txt"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not isinstance(data, str):
            try:
                import json
                data = json.dumps(data, indent=2, ensure_ascii=False)
            except Exception:
                data = str(data)
                
        formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(formatted_text)
        return f"Data successfully saved to {filename}"
        
    except Exception as e:
        return f"Error saving file: {str(e)}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)
