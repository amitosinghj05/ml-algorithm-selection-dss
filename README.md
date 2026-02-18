# ML Algorithm Decision Support System (DSS) — Agent + Rule Engine (Python)

## What this is
A Decision Support System (DSS) that recommends ML algorithms based on user needs.
It asks questions (problem type + constraints), scores candidate algorithms using rules, and outputs
top recommendations with reasons.

## Why this is not just "if/else"
This project is structured like a real DSS:
- **Knowledge Base**: algorithms and their properties in `data/algorithms.yaml`
- **Inference Engine**: scoring + reasoning in `dss/engine.py`
- **Agent (CLI)**: adaptive questioning in `dss/agent.py`
- **Tests**: deterministic ranking checks in `tests/`

## Setup
Create a venv (PyCharm does this automatically), then install:
```bash
pip install -r requirements.txt