# ML Algorithm Selection DSS

A domain-aware Decision Support System (DSS) for selecting machine learning algorithm families based on:

- Application domain  
- Data modality  
- Primary task type  
- Practical deployment constraints  

The system produces ranked algorithm family recommendations with explainable reasoning.

---

## Overview

Selecting the appropriate machine learning approach depends on multiple factors:

- **Data modality** (structured, text, image, time-series, multimodal)
- **Domain context** (healthcare, finance, cybersecurity, manufacturing, agriculture, etc.)
- **Task type** (classification, regression, clustering, anomaly detection)
- **Deployment constraints** (interpretability, privacy, limited labeled data, real-time requirements)

This system encodes these considerations into a structured, rule-based inference engine aligned with domain-specific ML trends.

---


## Key Features

- Domain-aware recommendations  
- Modality-driven scoring (primary decision factor)  
- Constraint-aware adjustments  
- Explainable ranking (traceable reasoning)  
- Exportable decision report  
- Unit-tested inference logic  



---

## Installation

Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

The application will open in your browser.

---

## Example Use Case

Example scenario:

- Domain: Finance  
- Data Modality: Structured / Tabular  
- Task: Classification  

The system prioritizes tree ensemble methods such as XGBoost and Random Forest and provides reasoning for the ranking based on modality and domain alignment.

---

## Extensibility

The system can be extended by:

- Adding new algorithm families in `knowledge_base.yaml`
- Adjusting scoring weights in `engine.py`
- Expanding constraint logic
- Incorporating additional domain mappings

---

## Purpose

This project demonstrates how literature-informed insights on algorithm dominance can be translated into a structured, explainable decision support system.
