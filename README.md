# Health Doctor GenAI — Intelligent Health Data Analysis System

A development-ready GenAI-driven health analytics engine that can interpret natural language questions from users, generate safe SQL queries dynamically, fetch structured health data, and produce medically safe, context-aware insights and lifestyle recommendations.

Built using FastAPI, PostgreSQL, SQLAlchemy, and a trusted LLM (OpenAI-compatible).
Designed with security, reliability, extendibility, and strict SQL-safety as top priorities.

---

# Project Structure Overview
```
health_doctor_genai/
├── main.py
├── apps
│   ├── routers.py          # API endpoints
│   ├── service.py          # LLM + SQL + answer orchestration
│   ├── sql_validator.py    # Security layer for SQL checks
│   ├── models.py           # Pydantic schemas
│   ├── persistence.py      # DB execution utilities
│   └── exceptions.py       # Custom exception classes
├── database
│   ├── connection.py       # PostgreSQL engine/session
│   ├── dependency.py       # FastAPI DB dependency
│   └── models.py           # SQLAlchemy ORM tables
├── scripts
│   └── init_health_data.py # Bulk CSV loader
├── data/
│   ├── health_dataset_1.csv
│   └── health_dataset_2.csv
├── loggers/
│   └── logger.py           # Central logging config
└── logs/                   # Runtime logs
```

---
## Technologies Used

| Component      | Technology                               |
| -------------- | ---------------------------------------- |
| Backend API    | **FastAPI**                              |
| Database       | **PostgreSQL + SQLAlchemy ORM**          |
| Data Loading   | Pandas + SQLAlchemy                      |
| AI Integration | OpenAI-compatible API (gpt-4o-mini etc.) |
| SQL Safety     | Custom SQL validation layer              |
| Logging        | Python logging framework                 |

---

# Health-Oriented Dataset Modeling

##Dataset 1 – Patient Health Profile
Hemoglobin
BMI
Genetic pedigree coefficient
Stress levels
Chronic kidney disease
Thyroid/adrenal disorders
Smoking/alcohol/salt consumption
Age, Sex, Pregnancy

##Dataset 2 – Patient Activity (10-day steps data)
Patient_Number
Day_Number
Physical_activity
Both datasets are stored in PostgreSQL and linked by Foreign Key.

---

# LLM-Generated Explanations with Medical Safety Guardrails

The LLM never gives medical advice.
Instead, it provides:
Analytical summary
General lifestyle recommendations
Mandatory disclaimer:
“This is not medical advice. Please consult a healthcare professional.”

---

# Fully Logged & Debuggable System

Query logs
SQL generation logs
Validation errors
Data ingestion logs
Essential for debugging, audits, and enterprise readiness.

---
