# apps/routers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.models import QueryRequest, QueryResponse
from apps.service import handle_query
from database.dependency import get_db  
from loggers.logger import get_logger
from apps.exceptions import (
    LLMError,
    SQLGenerationError,
    QueryExecutionError,
    NoDataFoundError,
)
logger = get_logger("api_router")

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_endpoint(payload: QueryRequest, db: Session = Depends(get_db)):
    try:
        result = handle_query(db, payload.question)
        return QueryResponse(**result)

    except SQLGenerationError as e:
        logger.warning(f"SQL generation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except NoDataFoundError as e:
        logger.info(f"No data found: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    except LLMError as e:
        logger.error(f"LLM error: {e}")
        raise HTTPException(status_code=502, detail="LLM service error")

    except QueryExecutionError as e:
        logger.error(f"Query execution error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")

    except Exception as e:
        logger.exception(f"Unexpected error in /query endpoint: {e}")
        raise HTTPException(status_code=500, detail="Unexpected server error")