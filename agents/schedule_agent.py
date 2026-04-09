from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


def run_schedule_builder(user_input: str, analysis: str) -> str:
    """
    Schedule Builder Agent — receives the analyzer's output and 
    creates a detailed, realistic day-by-day study timetable.
    """
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

    prompt = PromptTemplate.from_template("""
You are a study schedule expert AI agent. You receive analysis from another agent and build a timetable.

Original student situation: {input}

Analysis from Analyzer Agent:
{analysis}

Now create a complete study schedule. Include:

**DAY-BY-DAY PLAN:**
For each day, list time slots like:
  09:00 AM - 11:00 AM → Topic Name (what to cover exactly)
  11:00 AM - 11:15 AM → Short break
  11:15 AM - 01:00 PM → Topic Name (what to cover exactly)
  ...and so on

**DAILY TARGETS:**
What must be completed each day (non-negotiable)

**REVISION SLOTS:**
When to revise what was already studied

**BREAK SCHEDULE:**
Every 90-120 minutes include a 15-minute break. Include one meal break.

**NIGHT BEFORE EXAM:**
What to do the last evening before exam

**EXAM DAY TIP:**
One practical tip for exam day morning

Make the schedule realistic. Do not overload the student. 
Assume an average student who needs clear guidance.
""")

    chain = prompt | llm
    response = chain.invoke({"input": user_input, "analysis": analysis})
    return response.content