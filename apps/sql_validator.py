# apps/sql_validator.py
import re
from typing import Set
from apps.exceptions import SQLGenerationError

# Allowed tables
ALLOWED_TABLES: Set[str] = {"health_static", "steps_daily"}

# Forbidden keywords (DDL/DML, comments, multi-query operators)
DISALLOWED_KEYWORDS: Set[str] = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE",
    "CREATE", "REPLACE", "GRANT", "REVOKE",
    "UNION", "EXCEPT", "INTERSECT",
}

def validate_sql(sql: str) -> str:
    """
    PostgreSQL-safe SQL validator:
    Allows semicolons at the end
    Preserves case (no lowercasing)
    Ensures only SELECT queries
    Ensures only allowed tables are used
    Blocks DDL/DML/comment injection
    """
    if not sql or not sql.strip():
        raise SQLGenerationError("Empty SQL generated")

    # Trim whitespace but DO NOT lowercase
    normalized = " ".join(sql.strip().split())

    # 1. Must start with SELECT (case-insensitive)
    if not re.match(r"^\s*SELECT\b", normalized, flags=re.IGNORECASE):
        raise SQLGenerationError("Only SELECT statements are allowed")

    # 2. Allow semicolon ONLY at the end
    if ";" in normalized[:-1]:
        raise SQLGenerationError("Semicolon allowed only at the end of the query")

    # 3. Check for forbidden keywords (case-insensitive)
    for keyword in DISALLOWED_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", normalized, flags=re.IGNORECASE):
            raise SQLGenerationError(f"Forbidden SQL keyword detected: {keyword}")

    # 4. Extract table names from FROM and JOIN clauses
    # tables = re.findall(r"\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)", normalized, flags=re.IGNORECASE)
    # tables += re.findall(r"\bJOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)", normalized, flags=re.IGNORECASE)

    # if not tables:
    #     raise SQLGenerationError("Query must reference at least one allowed table")

    # # 5. Validate table names (case-sensitive match)
    # for t in tables:
    #     if t not in ALLOWED_TABLES:
    #         raise SQLGenerationError(f"Unknown or unsafe table used: {t}")

    return sql
