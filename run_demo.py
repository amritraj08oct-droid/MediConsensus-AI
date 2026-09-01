"""
MediConsensus AI
Multi-agent medical report analysis for educational/research use.

This project uses the Octochains orchestration framework to run isolated
specialist analyses in parallel and then combine them into a consensus report.
"""

import argparse
import datetime as dt
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from octochains import Agent, Engine
from octochains.aggregators import Synthesizer

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "medical_reports"
RESULT_DIR = BASE_DIR / "results"

load_dotenv(BASE_DIR / ".env")


def openai_llm_callable(prompt: str) -> str:
    """Generate one isolated specialist response using the configured LLM."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Create a .env file from .env.example."
        )

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
    llm = ChatOpenAI(
        temperature=0,
        model=model_name,
        api_key=api_key,
    )
    return llm.invoke(prompt).content


class CardiacAnalyst(Agent):
    def __init__(self):
        super().__init__(
            role="Cardiac Analyst",
            goal="Review cardiovascular clues without making a definitive diagnosis.",
            input_description="de-identified educational medical report",
            llm_callable=openai_llm_callable,
        )

    def execute(self, medical_report: str) -> str:
        prompt = f"""
You are the cardiac-analysis specialist in a multidisciplinary AI workflow.
Review ONLY the supplied educational medical report.

Look for:
- cardiovascular symptoms or risk factors
- ECG, blood-pressure, cardiac-marker, Holter, or echocardiogram clues
- findings that could reasonably warrant follow-up

Return:
1. Relevant cardiac evidence
2. Possible interpretations (not diagnoses)
3. Suggested questions/tests for a licensed clinician

Do not invent missing measurements or claim certainty.

REPORT:
{medical_report}
"""
        return self.llm_callable(prompt)


class MentalWellnessAnalyst(Agent):
    def __init__(self):
        super().__init__(
            role="Mental Wellness Analyst",
            goal="Identify psychological and behavioral factors that may be relevant to the reported symptoms.",
            input_description="de-identified educational medical report",
            llm_callable=openai_llm_callable,
        )

    def execute(self, medical_report: str) -> str:
        prompt = f"""
You are the mental-wellness specialist in a multidisciplinary AI workflow.
Review ONLY the supplied educational medical report.

Look for:
- documented anxiety, mood, sleep, stress, or behavioral clues
- symptom patterns that may have psychological or behavioral contributors
- important uncertainty or missing context

Return:
1. Relevant evidence
2. Possible interpretations (not diagnoses)
3. Suggested clinician follow-up

Do not label the patient with a disorder unless the report explicitly documents it.

REPORT:
{medical_report}
"""
        return self.llm_callable(prompt)


class RespiratoryAnalyst(Agent):
    def __init__(self):
        super().__init__(
            role="Respiratory Analyst",
            goal="Review respiratory signs and identify information that may need pulmonary follow-up.",
            input_description="de-identified educational medical report",
            llm_callable=openai_llm_callable,
        )

    def execute(self, medical_report: str) -> str:
        prompt = f"""
You are the respiratory-analysis specialist in a multidisciplinary AI workflow.
Review ONLY the supplied educational medical report.

Look for:
- breathing, oxygenation, cough, wheeze, or chest-related clues
- pulmonary-function or imaging information
- evidence that could justify additional clinical review

Return:
1. Relevant respiratory evidence
2. Possible interpretations (not diagnoses)
3. Suggested clinician follow-up

Do not invent findings or provide treatment instructions.

REPORT:
{medical_report}
"""
        return self.llm_callable(prompt)


def choose_report() -> Path:
    reports = sorted(REPORT_DIR.glob("*.txt"))
    if not reports:
        raise FileNotFoundError(f"No .txt reports found in {REPORT_DIR}")

    print("\nAvailable educational cases:")
    for i, path in enumerate(reports, 1):
        print(f"  {i}. {path.name}")

    while True:
        choice = input(f"Select a case [1-{len(reports)}]: ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(reports):
                return reports[index]
        except ValueError:
            pass
        print("Please enter a valid case number.")


def save_consensus(consensus, report_name: str) -> Path:
    RESULT_DIR.mkdir(exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = RESULT_DIR / "latest_consensus.md"

    with output.open("w", encoding="utf-8") as f:
        f.write("# MediConsensus AI — Educational Consensus Report\n\n")
        f.write(f"**Source case:** `{report_name}`\n\n")
        f.write(f"**Generated:** {timestamp}\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"{consensus.narrative}\n\n")
        f.write("## Key Takeaways\n\n")
        for item in consensus.key_takeaways:
            f.write(f"- {item}\n")
        f.write("\n## Specialist Evidence\n\n")
        for role, snippet in consensus.citations.items():
            f.write(f"- **{role}:** {snippet}\n")
        f.write(f"\n**Consensus confidence:** {consensus.confidence:.0%}\n")
        f.write(
            "\n> Educational/research output only. This is not a medical diagnosis "
            "and must not be used to make treatment decisions.\n"
        )

    return output


def main():
    parser = argparse.ArgumentParser(description="Run MediConsensus AI.")
    parser.add_argument(
        "--case",
        type=str,
        help="Path to a .txt case file. If omitted, choose interactively.",
    )
    args = parser.parse_args()

    report_path = Path(args.case).expanduser().resolve() if args.case else choose_report()
    if not report_path.exists():
        raise FileNotFoundError(f"Case file not found: {report_path}")

    patient_data = report_path.read_text(encoding="utf-8")

    specialists = [
        CardiacAnalyst(),
        MentalWellnessAnalyst(),
        RespiratoryAnalyst(),
    ]

    coordinator = Synthesizer(
        llm_callable=openai_llm_callable,
        custom_goal=(
            "Create a cautious multidisciplinary educational synthesis. "
            "Separate documented evidence from interpretation, highlight uncertainty, "
            "and list three priority follow-up considerations. Never present the "
            "output as a definitive diagnosis or treatment plan."
        ),
    )

    engine = Engine(agents=specialists, aggregator=coordinator)

    print("\n🩺 MediConsensus AI")
    print("=" * 64)
    print(f"Case: {report_path.name}")
    print("Running isolated specialist analyses...")

    report = engine.run(patient_data, show_log=True)
    consensus = report.consensus

    print("\n" + "=" * 64)
    print("MULTIDISCIPLINARY EDUCATIONAL CONSENSUS")
    print("=" * 64)

    if hasattr(consensus, "narrative"):
        print(f"\n[SUMMARY]\n{consensus.narrative}")
        print("\n[KEY TAKEAWAYS]")
        for i, item in enumerate(consensus.key_takeaways, 1):
            print(f"{i}. {item}")
        print(f"\n[CONFIDENCE] {consensus.confidence:.0%}")

        saved = save_consensus(consensus, report_path.name)
        print(f"\n✅ Report saved to: {saved}")
    else:
        print(consensus)


if __name__ == "__main__":
    main()
