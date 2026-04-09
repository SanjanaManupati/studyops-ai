"""
Orchestrator — the brain of StudyOps AI.
It controls which agent runs when, passes outputs between agents,
and returns the complete result. This is the handoff pattern in Agentic AI.
"""

from agents.analyzer_agent import run_analyzer
from agents.schedule_agent import run_schedule_builder
from agents.resource_agent import run_resource_finder
from agents.notifier_agent import send_telegram_notification


def run_studyops(user_input: str, notify: bool = False) -> dict:
    """
    Main orchestration function.
    
    Flow:
    1. Analyzer Agent   → understands the problem
    2. Schedule Agent   → builds plan (uses analyzer output)
    3. Resource Agent   → finds study materials
    4. Notifier Agent   → sends Telegram (optional)
    
    Returns a dict with all results.
    """

    results = {}

    # ─── AGENT 1: Analyzer ───────────────────────────────────────────────
    print("🔍 [Orchestrator] Starting Analyzer Agent...")
    analysis = run_analyzer(user_input)
    results["analysis"] = analysis
    print("✅ [Orchestrator] Analyzer Agent complete. Passing output to Schedule Agent...")

    # ─── AGENT 2: Schedule Builder ────────────────────────────────────────
    # NOTE: This agent receives the ANALYSIS output — this is the HANDOFF
    print("📅 [Orchestrator] Starting Schedule Builder Agent...")
    schedule = run_schedule_builder(user_input, analysis)
    results["schedule"] = schedule
    print("✅ [Orchestrator] Schedule Agent complete. Passing to Resource Agent...")

    # ─── AGENT 3: Resource Finder ─────────────────────────────────────────
    print("🔎 [Orchestrator] Starting Resource Finder Agent (DuckDuckGo)...")
    resources = run_resource_finder(user_input)
    results["resources"] = resources
    print("✅ [Orchestrator] Resource Agent complete.")

    # ─── AGENT 4: Notifier (optional) ────────────────────────────────────
    if notify:
        print("📱 [Orchestrator] Starting Notifier Agent (Telegram)...")
        notification_status = send_telegram_notification(analysis, schedule, resources)
        results["notification"] = notification_status
        print(f"✅ [Orchestrator] Notifier Agent: {notification_status}")

    print("🏁 [Orchestrator] All agents complete. Returning results.")
    return results


if __name__ == "__main__":
    # Quick test — run this file directly to test without UI
    test_input = "I have an exam in 2 days on Operating Systems and DBMS. I am weak in Process Scheduling and SQL. I can study 8 hours a day."
    print("Running StudyOps AI test...\n")
    results = run_studyops(test_input, notify=False)
    print("\n=== ANALYSIS ===")
    print(results["analysis"])
    print("\n=== SCHEDULE ===")
    print(results["schedule"])
    print("\n=== RESOURCES ===")
    print(results["resources"])