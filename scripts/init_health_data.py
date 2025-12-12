# scripts/init_health_data.py
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import sessionmaker
from database.connection import engine
from database.models import HealthStatic, StepsDaily
from database.models import Base

# allow top-level imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))


DATA_DIR = ROOT / "data"
# possible file name variations (choose the first that exists)
FILE1_CANDIDATES = [
    "health_dataset_1.csv",
    "Health Dataset 1 (N=2000).csv",
    "Health Dataset 1.csv"
]
FILE2_CANDIDATES = [
    "health_dataset_2.csv",
    "Health Dataset 2 (N=20000).csv",
    "Health Dataset 2.csv"
]


def _find_existing_file(candidates):
    for f in candidates:
        p = DATA_DIR / f
        if p.exists():
            return p
    raise FileNotFoundError(f"No candidate file found in {DATA_DIR} for {candidates}")


def load_health_static_via_pandas():
    path = _find_existing_file(FILE1_CANDIDATES)
    print("Loading", path)
    df = pd.read_csv(path)
    # optional: rename columns to match model if CSV has odd whitespace
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    # write using SQLAlchemy engine (fast for bulk)
    df.to_sql("health_static", engine, if_exists="append", index=False)
    print("Inserted", len(df), "rows into health_static")


def load_steps_daily_via_pandas():
    path = _find_existing_file(FILE2_CANDIDATES)
    print("Loading", path)
    df = pd.read_csv(path)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    df.to_sql("steps_daily", engine, if_exists="append", index=False)
    print("Inserted", len(df), "rows into steps_daily")


def main():
    SessionLocal = sessionmaker(bind=engine)
    # ensure tables exist before writing
    Base.metadata.create_all(bind=engine)

    load_health_static_via_pandas()
    load_steps_daily_via_pandas()
    print("Done")


if __name__ == "__main__":
    main()
