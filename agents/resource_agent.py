from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


def run_resource_finder(user_input: str) -> str:
    """
    Resource Finder Agent — uses DuckDuckGo (no API key needed, completely free)
    to find real study resources, then summarizes them using the LLM.
    """

    # Search DuckDuckGo for free study resources
    search_results_text = ""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                f"free study resources tutorials for {user_input} students",
                max_results=6
            ))
            for r in results:
                search_results_text += f"- {r['title']}: {r['href']}\n  {r['body'][:100]}\n\n"
    except Exception as e:
        search_results_text = f"Search unavailable: {str(e)}"

    # Also search YouTube specifically
    youtube_results_text = ""
    try:
        with DDGS() as ddgs:
            yt_results = list(ddgs.text(
                f"youtube free lecture {user_input} exam preparation",
                max_results=4
            ))
            for r in yt_results:
                youtube_results_text += f"- {r['title']}: {r['href']}\n"
    except Exception:
        youtube_results_text = "YouTube search unavailable."

    # Use LLM to present resources clearly
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

    prompt = PromptTemplate.from_template("""
You are a resource finder AI agent. You found these real search results for a student.

Student's topics: {input}

Web search results:
{web_results}

YouTube search results:
{yt_results}

Now present the best resources clearly in this format:

**TOP FREE WEBSITES:**
List 3-4 best websites with their URLs and what they cover.

**YOUTUBE CHANNELS / VIDEOS:**
List 2-3 relevant YouTube resources with links.

**QUICK STUDY TIPS FOR THESE TOPICS:**
Give 3 specific tips that help with the exact topics mentioned.

**FREE TOOLS TO USE:**
Any free apps, tools, or platforms useful for these subjects.

Keep it short, practical, and directly useful. Include actual URLs where available.
""")

    chain = prompt | llm
    response = chain.invoke({
        "input": user_input,
        "web_results": search_results_text,
        "yt_results": youtube_results_text
    })
    return response.content