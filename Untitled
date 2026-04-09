import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyOps AI",
    page_icon="🧠",
    layout="wide"
)

# ─── Header ──────────────────────────────────────────────────────────────────
st.title("🧠 StudyOps AI")
st.subheader("Multi-Agent Study Decision System")

st.markdown("""
> **How it works:** You describe your study situation → 3 specialized AI agents analyze it, 
build your schedule, and find free resources → Optional Telegram notification sent to your phone.
""")

st.markdown("---")

# ─── Sidebar — Agent Status Panel ────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Agent Pipeline")
    st.markdown("""
    **Agent 1 → Analyzer**  
    Identifies weak topics, urgency, difficulty scores

    **Agent 2 → Schedule Builder**  
    *(receives Agent 1 output)*  
    Creates day-by-day timetable

    **Agent 3 → Resource Finder**  
    Uses DuckDuckGo to find free study material

    **Agent 4 → Notifier**  
    Sends plan to your Telegram
    """)
    st.markdown("---")
    st.markdown("**Tech Stack**")
    st.markdown("""
    - 🤖 Groq API (Llama 3) — Free LLM
    - 🔗 LangChain — Agent orchestration
    - 🔍 DuckDuckGo — Free web search
    - 📱 Telegram Bot — Free notifications
    - 📊 LangSmith — Agent tracing
    """)

# ─── Main Input Form ──────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Tell me your situation")
    user_input = st.text_area(
        label="Describe your exam situation in detail:",
        placeholder=(
            "Example:\n"
            "I have an exam in 2 days on Operating Systems and DBMS.\n"
            "I am weak in Process Scheduling, Deadlocks, and SQL Joins.\n"
            "I can study for 8 hours per day."
        ),
        height=160,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### Options")
    notify = st.checkbox(
        "📱 Send plan to Telegram",
        value=False,
        help="Sends your full study plan to your Telegram. Configure TELEGRAM_BOT_TOKEN in .env first."
    )
    st.markdown(" ")
    st.markdown(" ")
    run_button = st.button(
        "🚀 Generate Study Plan",
        use_container_width=True,
        type="primary"
    )

st.markdown("---")

# ─── Run agents when button clicked ──────────────────────────────────────────
if run_button:
    if not user_input.strip():
        st.warning("⚠️ Please describe your study situation in the text box above.")
    elif not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "paste_your_groq_key_here":
        st.error("❌ GROQ_API_KEY not set. Open your .env file and paste your Groq API key. Then restart the app.")
    else:
        # ── Agent status row ───────────────────────────────────────────────
        st.markdown("### 🔄 Running Agents...")
        agent_col1, agent_col2, agent_col3 = st.columns(3)

        # Run agents one by one — showing status
        analysis, schedule, resources = None, None, None

        with agent_col1:
            with st.spinner("🔍 Analyzer Agent running..."):
                try:
                    from agents.analyzer_agent import run_analyzer
                    analysis = run_analyzer(user_input)
                    st.success("✅ Analyzer Agent done")
                except Exception as e:
                    st.error(f"❌ Analyzer failed: {str(e)}")

        with agent_col2:
            if analysis:
                with st.spinner("📅 Schedule Agent running..."):
                    try:
                        from agents.schedule_agent import run_schedule_builder
                        schedule = run_schedule_builder(user_input, analysis)
                        st.success("✅ Schedule Agent done")
                    except Exception as e:
                        st.error(f"❌ Schedule failed: {str(e)}")

        with agent_col3:
            if analysis:
                with st.spinner("🔎 Resource Agent running..."):
                    try:
                        from agents.resource_agent import run_resource_finder
                        resources = run_resource_finder(user_input)
                        st.success("✅ Resource Agent done")
                    except Exception as e:
                        st.error(f"❌ Resource finder failed: {str(e)}")

        # ── Display Results ────────────────────────────────────────────────
        if analysis and schedule and resources:
            st.markdown("---")
            st.markdown("## 📋 Your Personalized Study Plan")

            tab1, tab2, tab3 = st.tabs([
                "🔍 Analysis",
                "📅 Day-by-Day Schedule",
                "📚 Free Resources"
            ])

            with tab1:
                st.markdown("### What the Analyzer Agent Found")
                st.markdown(analysis)

            with tab2:
                st.markdown("### Your Complete Study Schedule")
                st.markdown(schedule)

            with tab3:
                st.markdown("### Free Study Resources (Found via DuckDuckGo)")
                st.markdown(resources)

            # ── Telegram notification ──────────────────────────────────────
            if notify:
                st.markdown("---")
                with st.spinner("📱 Notifier Agent sending to Telegram..."):
                    try:
                        from agents.notifier_agent import send_telegram_notification
                        status = send_telegram_notification(analysis, schedule, resources)
                        if status.startswith("✅"):
                            st.success(status)
                        else:
                            st.warning(status)
                    except Exception as e:
                        st.error(f"❌ Telegram error: {str(e)}")

            st.markdown("---")
            st.caption(
                "StudyOps AI | Built with LangChain + Groq Llama 3 + DuckDuckGo + Telegram Bot API | "
                "Agentic AI Training Project"
            )

# ─── Empty state ──────────────────────────────────────────────────────────────
else:
    st.markdown("""
    ### 👆 Enter your study situation above and click Generate

    **Example inputs to try:**
    - *"Exam in 2 days. Weak in OS scheduling and DBMS normalization. 8 hours available daily."*
    - *"3 days before Data Structures exam. Trees and Graphs are my weak areas."*
    - *"Tomorrow I have Computer Networks exam. Very weak in everything. 5 hours left."*
    """)