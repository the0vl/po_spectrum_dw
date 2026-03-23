import os
import glob
import json
import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger("RedditTransformer")


def get_latest_reddit_raw_file():
    """Finds the most recent Reddit JSON file in the raw directory."""
    files = glob.glob("data/raw/reddit_posts_*.json")
    if not files:
        logger.warning("No Reddit raw files found in data/raw/")
        return None
    return max(files, key=os.path.getctime)


def transform_reddit_data(file_path):
    """Cleans and flattens Reddit JSON into a DataFrame."""
    logger.info(f"Transforming: {file_path}")

    try:
        with open(file_path) as f:
            posts = json.load(f)
        if not posts:
            logger.warning("Empty post list in file")
            return None

        df = pd.DataFrame(posts)
        df["created_at"] = pd.to_datetime(df["created_utc"], unit="s")
        df["processed_at"] = datetime.now().isoformat()
        df["source_file"] = os.path.basename(file_path)
        return df
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        return None


def save_to_silver(df):
    """Saves the cleaned data to the data/processed directory."""
    if df is not None:
        os.makedirs("data/processed", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/processed/reddit_posts_silver_{timestamp}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Silver layer updated: {output_path}")


if __name__ == "__main__":
    latest_file = get_latest_reddit_raw_file()
    if latest_file:
        cleaned_df = transform_reddit_data(latest_file)
        save_to_silver(cleaned_df)
