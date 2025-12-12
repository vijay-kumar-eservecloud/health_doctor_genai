# apps/service.py
import json
import os
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

from apps.persistence import execute_raw_sql
from apps.sql_validator import validate_sql
from apps.exceptions import (
    LLMError,
    QueryExecutionError,
    NoDataFoundError,
)
from loggers.logger import get_logger

logger = get_logger("service")

# 1) DB schema as text (for LLM)
DB_SCHEMA = """
TABLE health_static (
  Patient_Number BIGINT,
  Blood_Pressure_Abnormality INTEGER,
  Level_of_Hemoglobin FLOAT,
  Genetic_Pedigree_Coefficient FLOAT,
  Age INTEGER,
  BMI FLOAT,
  Sex INTEGER,
  Pregnancy INTEGER,
  Smoking INTEGER,
  salt_content_in_the_diet FLOAT,
  alcohol_consumption_per_day FLOAT,
  Level_of_Stress INTEGER,
  Chronic_kidney_disease INTEGER,
  Adrenal_and_thyroid_disorders INTEGER
);

TABLE steps_daily (
  id BIGINT,
  Patient_Number BIGINT,
  Day_Number INTEGER,
  Physical_activity INTEGER
);
"""

# 2) LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except OpenAIError as e:
        logger.exception("LLM call failed")
        raise LLMError(str(e))


# 3) SQL generation
SQL_SYSTEM_PROMPT = f"""
You are a data analyst. You must generate a single, read-only SQL query
for a PostgreSQL database, based strictly on the schema provided.

Rules:
- Use ONLY SELECT statements.
- NEVER use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
  CREATE, REPLACE, GRANT, REVOKE or any statement that modifies data or schema.
- Use only the tables and columns listed in the schema.
- Join health_static and steps_daily on Patient_Number when needed.
- The output MUST be valid PostgreSQL syntax.
- Do NOT include explanations, comments, or markdown. Return ONLY the raw SQL query.
IMPORTANT:
PostgreSQL column names in this schema contain capital letters.
You MUST wrap all table and column names in double quotes, for example "BMI", "Sex", "Age".
If you do not use double quotes, the query will fail.
Always output valid PostgreSQL syntax.
Schema:
{DB_SCHEMA}
"""

def generate_sql_from_question(question: str) -> str:
    user_prompt = f"""
User question:
{question}

Return a SINGLE PostgreSQL SELECT query, no comments, no markdown, no explanation.
"""
    sql = call_llm(SQL_SYSTEM_PROMPT, user_prompt)
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # Safety & sanity checks
    sql = validate_sql(sql)  # raises SQLGenerationError if unsafe/invalid

    logger.info(f"Generated safe SQL for question '{question}': {sql}")
    return sql


# 4) Answer generation
ANSWER_SYSTEM_PROMPT = """
You are a medical data analyst (not a doctor).
Given a user question, the SQL that was executed, and the SQL result rows:

Your task:
1. Describe what the data shows in clear, non-technical language.
2. Do NOT provide any medical advice, diagnosis, or lifestyle recommendations.
3. Do NOT speculate beyond what is directly supported by the data.
4. Always end with: "This is not medical advice. Please consult a healthcare professional."

Only explain the data returned by the query.
"""

def generate_answer(question: str, sql: str, rows: List[Dict[str, Any]]) -> str:
    user_prompt = f"""
User question:
{question}

SQL executed:
{sql}

Result rows (JSON):
{json.dumps(rows, indent=2)}
"""
    answer = call_llm(ANSWER_SYSTEM_PROMPT, user_prompt)
    logger.info(f"Generated answer for question '{question}'")
    return answer


# 5) Orchestrator used by router
def handle_query(db: Session, question: str) -> Dict[str, Any]:
    # a) NL → safe SQL
    sql = generate_sql_from_question(question)

    # b) Execute SQL
    try:
        rows = execute_raw_sql(db, sql)
    except Exception as e:
        logger.exception("SQL execution error")
        raise QueryExecutionError(str(e))

    if not rows:
        logger.info("No rows returned for query")
        raise NoDataFoundError()

    # c) Rows → explanation (data-only)
    answer = generate_answer(question, sql, rows)

    return {
        "question": question,
        "sql": sql,
        "result": rows,
        "answer": answer,
    }
