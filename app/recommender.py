import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.database import SessionLocal
from app.models import Trek

def get_all_treks_df():
    """Fetch all treks from database into DataFrame"""
    session = SessionLocal()
    treks = session.query(Trek).all()
    session.close()
    df = pd.DataFrame([{
        "id": t.id,
        "name": t.name,
        "region": t.region,
        "difficulty": t.difficulty.lower(),
        "cost_usd": t.cost_usd,
        "duration_days": t.duration_days,
        "bestTimeToTravel": t.bestTimeToTravel.lower(),
        "information": t.information.lower(),
    } for t in treks])
    return df


def recommend_treks(cost: float, duration: int, month: str, difficulty: str, top_n: int = 5):
    """Hybrid content-based + weighted scoring recommendation"""
    df = get_all_treks_df()
    if df.empty:
        return []

    # --- Step 1: Content-Based Similarity ---
    df["combined_features"] = (
        df["region"].astype(str) + " " +
        df["difficulty"].astype(str) + " " +
        df["bestTimeToTravel"].astype(str) + " " +
        df["information"].astype(str)
    )

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(tfidf_matrix)

    # We’ll simulate user preference vector using the input filters
    user_query = f"{difficulty} {month}"
    user_vec = vectorizer.transform([user_query])
    content_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()

    # --- Step 2: Weighted Numeric Scoring ---
    # Normalize numeric differences (smaller diff = higher score)
    cost_diff = np.abs(df["cost_usd"] - cost)
    duration_diff = np.abs(df["duration_days"] - duration)

    # Prevent division by zero
    df["cost_score"] = 1 / (1 + cost_diff / cost)  # closer to budget → higher
    df["duration_score"] = 1 / (1 + duration_diff / duration)

    # Month match bonus (if user's month appears in bestTimeToTravel)
    df["month_match"] = df["bestTimeToTravel"].apply(lambda x: 1 if month.lower() in x else 0)

    # Difficulty match bonus
    df["difficulty_match"] = df["difficulty"].apply(lambda x: 1 if x == difficulty.lower() else 0)

    # --- Step 3: Weighted Combination ---
    # You can tune these weights to your preference
    w_content = 0.4
    w_cost = 0.25
    w_duration = 0.2
    w_month = 0.1
    w_difficulty = 0.05

    df["final_score"] = (
        w_content * content_scores +
        w_cost * df["cost_score"] +
        w_duration * df["duration_score"] +
        w_month * df["month_match"] +
        w_difficulty * df["difficulty_match"]
    )

    df_sorted = df.sort_values(by="final_score", ascending=False).head(top_n)

    # Return only the necessary details
    recommendations = df_sorted[["id", "name", "region", "difficulty", "cost_usd", "duration_days", "bestTimeToTravel"]].to_dict(orient="records")
    return recommendations
