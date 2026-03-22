import os
import glob
import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger("Transformer")

def get_latest_raw_file():
    """Finds the most recent JSON file in the raw directory."""
    files = glob.glob('data/raw/*.json')
    if not files:
        logger.warning("No raw files found in data/raw/")
        return None
    # Returns the file with the latest creation time
    return max(files, key=os.path.getctime)

def transform_data(file_path):
    """Cleans and flattens the raw JSON data into a DataFrame."""
    logger.info(f"Transforming: {file_path}")
    
    try:
        # 1. Read the JSON
        df = pd.read_json(file_path)
        
        # 2. Transpose (Turn keys into rows)
        df = df.T 
        df.index.name = 'ticker'
        df = df.reset_index()
        
        # 3. Add metadata (audit columns)
        df['processed_at'] = datetime.now().isoformat()
        df['source_file'] = os.path.basename(file_path)
        
        return df
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        return None

def save_to_silver(df):
    """Saves the cleaned data to the data/processed directory."""
    if df is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/processed/market_data_silver_{timestamp}.csv"
        
        df.to_csv(output_path, index=False)
        logger.info(f"Silver layer updated: {output_path}")

if __name__ == "__main__":
    latest_file = get_latest_raw_file()
    
    if latest_file:
        cleaned_df = transform_data(latest_file)
        save_to_silver(cleaned_df)