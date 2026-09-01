# 🩺 MediConsensus AI

### Multi-Agent Medical Report Analysis & Consensus

MediConsensus AI is an educational multi-agent system that sends the same
medical case to several **isolated specialist agents in parallel**, then uses
a separate coordinator to combine their observations into one cautious
consensus report.

> ⚠️ **Educational/research project only. It is not a medical diagnostic tool,
does not replace a qualified healthcare professional, and must not be used
to make treatment decisions.**

## ✨ What makes this version different?

This repository is a customized educational project derived from the
**Octochains** medical-diagnostics example. The workflow has been reorganized
around three analysis roles:

- ❤️ **Cardiac Analyst** — cardiovascular evidence and follow-up considerations
- 🧠 **Mental Wellness Analyst** — psychological/behavioral context
- 🫁 **Respiratory Analyst** — respiratory evidence and pulmonary follow-up
- 🧩 **Consensus Coordinator** — combines independent outputs while preserving uncertainty

The application also includes:

- secure `.env` API-key loading
- cross-platform report paths using `pathlib`
- interactive case selection
- optional `--case` command-line input
- Markdown consensus report generation
- explicit educational safety framing

## 🧪 Testing & API Key Requirement

The complete workflow is intended to be tested end-to-end using **your own valid OpenAI API key**. Because the specialist agents and consensus coordinator make live API requests, successful execution depends on a valid, active API key and the corresponding API account having access to the selected model.

> **Note:** This repository does not include or claim to contain a live API key. Before running the project, configure your own key in `.env` as described below. Do not commit or publish the key.

## 🏗️ Workflow

```text
                 ┌─────────────────────┐
                 │  Educational Case    │
                 │      (.txt)          │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │  Cardiac   │ │   Mental   │ │ Respiratory│
      │  Analyst   │ │  Wellness  │ │  Analyst   │
      └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Consensus Coordinator│
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Markdown Report     │
                 │ results/latest...   │
                 └─────────────────────┘
```

## 🚀 Setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Copy `.env.example` to `.env`:

```text
OPENAI_API_KEY=your_api_key_here
```

**Never commit `.env` or expose your API key on GitHub.**

### 4. Run

Interactive case picker:

```bash
python run_demo.py
```

Or specify a case:

```bash
python run_demo.py --case "medical_reports/case_David_Wilson_Alzheimer_s_Disease.txt"
```

A successful run writes the latest consensus to:

```text
results/latest_consensus.md
```

## 📁 Project structure

```text
MediConsensus-AI/
├── medical_reports/       # educational sample cases
├── results/               # generated reports (ignored by Git)
├── .env.example
├── .gitignore
├── requirements.txt
├── run_demo.py
└── README.md
```

## 🔐 API-key safety

This project intentionally does **not** contain a real API key.

If a key has ever been pasted into source code, a terminal log, a chat, or a
public repository, revoke/rotate it before continuing.

## 📜 Attribution & licensing

This project is a customized educational derivative of the medical-diagnostics
example from **Octochains**.

Original framework:
https://github.com/AhmadVh7/octochains

Please retain and comply with the original Octochains license and proprietary
notices when using or redistributing code derived from it. This repository
does not claim ownership of the underlying Octochains framework.

## ⚖️ Disclaimer

The generated output is experimental AI text for learning/research. It can be
incorrect, incomplete, or misleading. It must not be interpreted as a medical
diagnosis, treatment recommendation, or emergency guidance.
