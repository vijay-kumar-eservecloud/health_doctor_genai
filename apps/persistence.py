# apps/persistence.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from apps.exceptions import QueryExecutionError
from loggers.logger import get_logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from decimal import Decimal

logger = get_logger("persistence")




def _convert_decimal(obj: Any):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def execute_raw_sql(db: Session, sql: str) -> List[Dict[str, Any]]:
    try:
        result = db.execute(text(sql))
        rows = result.mappings().all()

        # Convert each row, ensuring Decimal → float
        clean_rows = []
        for row in rows:
            clean_row = {k: _convert_decimal(v) for k, v in row.items()}
            clean_rows.append(clean_row)

        return clean_rows

    except SQLAlchemyError as e:
        logger.exception("DB error while executing SQL")
        raise QueryExecutionError(str(e))