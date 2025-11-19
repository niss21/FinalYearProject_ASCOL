import pandas as pd
import os
from .database import Base, engine, DB_PATH
from .models import Trek

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'treks.csv')


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


def load_csv_to_db(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path)

    # Normalize column names if needed
    expected_cols = ['name','images','region','duration_days','difficulty','permitRequired','cost_usd',
                     'information','keyPoints','tourHighlights','bestTimeToTravel','detailedItinerary']
    for c in expected_cols:
        if c not in df.columns:
            print(f"Warning: column {c} missing in CSV; filling with None")
            df[c] = None

    session = None
    from sqlalchemy.orm import Session
    session = Session(bind=engine)

    # Optionally clear existing
    session.query(Trek).delete()
    session.commit()

    for _, row in df.iterrows():
        trek = Trek(
            name = str(row.get('name')) if not pd.isna(row.get('name')) else None,
            images = str(row.get('images')) if not pd.isna(row.get('images')) else None,
            region = str(row.get('region')) if not pd.isna(row.get('region')) else None,
            duration_days = int(row.get('duration_days')) if not pd.isna(row.get('duration_days')) else None,
            difficulty = str(row.get('difficulty')) if not pd.isna(row.get('difficulty')) else None,
            permitRequired = bool(row.get('permitRequired')) if not pd.isna(row.get('permitRequired')) else False,
            cost_usd = float(row.get('cost_usd')) if not pd.isna(row.get('cost_usd')) else None,
            information = str(row.get('information')) if not pd.isna(row.get('information')) else None,
            keyPoints = str(row.get('keyPoints')) if not pd.isna(row.get('keyPoints')) else None,
            tourHighlights = str(row.get('tourHighlights')) if not pd.isna(row.get('tourHighlights')) else None,
            bestTimeToTravel = str(row.get('bestTimeToTravel')) if not pd.isna(row.get('bestTimeToTravel')) else None,
            detailedItinerary = str(row.get('detailedItinerary')) if not pd.isna(row.get('detailedItinerary')) else None,
        )
        session.add(trek)
    session.commit()
    print("Database populated with treks from CSV.")


if __name__ == '__main__':
    create_db_and_tables()
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at {CSV_PATH}. Place your treks.csv there and rerun.")
    else:
        load_csv_to_db()
