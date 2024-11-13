import streamlit as st
from swarm import Swarm, Agent
from duckduckgo_search import DDGS
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use GPT-3.5-turbo model
MODEL = "gpt-3.5-turbo"

# Initialize Swarm client
client = Swarm()

# DuckDuckGo search instance
ddgs = DDGS()

# Function to search the web using DuckDuckGo
def search_web(query):
    print(f"Searching the web for {query}...")
    
    # DuckDuckGo search
    current_date = datetime.now().strftime("%Y-%m")
    results = ddgs.text(f"{query} {current_date}", max_results=10)
    if results:
        news_results = ""
        for result in results:
            news_results += f"Title: {result['title']}\nURL: {result['href']}\nDescription: {result['body']}\n\n"
        return news_results.strip()
    else:
        return f"Could not find news results for {query}."
    

# Define the Web Search Agent
web_search_agent = Agent(
    name="Web Search Assistant",
    instructions="Your role is to gather latest news articles on specified topics using DuckDuckGo's search capabilities.",
    functions=[search_web],
    model=MODEL
)

# Define the Research Analyst Agent
researcher_agent = Agent(
    name="Research Assistant",
    instructions="""Your role is to analyze and synthesize the raw search results. You should:
    1. Remove duplicate information and redundant content
    2. Identify and merge related topics and themes
    3. Verify information consistency across sources
    4. Prioritize recent and relevant information
    5. Extract key facts, statistics, and quotes
    6. Identify primary sources when available
    7. Flag any contradictory information
    8. Maintain proper attribution for important claims
    9. Organize information in a logical sequence
    10. Preserve important context and relationships between topics""",
    model=MODEL
)

# Define the Editor Agent
writer_agent = Agent(
    name="Writer Assistant",
    instructions="""Your role is to transform the deduplicated research results into a polished, publication-ready article. You should:
    1. Organize content into clear, thematic sections
    2. Write in a professional yet engaging tone
    3. Ensure proper flow between topics
    4. Add relevant context where needed
    5. Maintain factual accuracy while making complex topics accessible
    6. Include a brief summary at the beginning
    7. Format with clear headlines and subheadings
    8. Preserve all key information from the source material""",
    model=MODEL
)

# Workflow function to run the agents
def run_workflow(query):
    print("Running web research assistant workflow...")
    
    # Step 1: Web Search
    news_response = client.run(
        agent=web_search_agent,
        messages=[{"role": "user", "content": f"Search the web for {query}"}],
    )
    
    raw_news = news_response.messages[-1]["content"]

    # Step 2: Analyze and Synthesize the Search Results
    research_analysis_response = client.run(
        agent=researcher_agent,
        messages=[{"role": "user", "content": raw_news }],
    )

    deduplicated_news = research_analysis_response.messages[-1]["content"]
    
    # Step 3: Edit and Format the Analyzed Results
