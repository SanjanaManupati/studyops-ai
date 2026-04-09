from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


def run_analyzer(user_input: str) -> str:
    """
    Analyzer Agent — reads the student's situation and identifies
    weak topics, urgency level, and difficulty scores.
    """
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

    prompt = PromptTemplate.from_template("""
You are an expert study coach AI agent. Your job is to carefully analyze a student's situation.

Student says: {input}

Provide a clear analysis with these sections:

**URGENCY LEVEL:** (High / Medium / Low)
Reason: explain why

**WEAK TOPICS IDENTIFIED:**
List every topic or subject the student mentioned being weak in.

**DIFFICULTY SCORE:**
Rate each weak topic from 1 to 10 (10 = hardest).

**RECOMMENDED FOCUS ORDER:**
Which topic should they study first and why?

**TIME ASSESSMENT:**
How many hours are available and is it enough?

Be specific, direct, and practical. Do not give vague advice.
""")

    chain = prompt | llm
    response = chain.invoke({"input": user_input})
    return response.content