import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from src.utils.logger import get_logger  # Import our new tool

# Initialize the logger for this specific script
logger = get_logger("Producer")

load_dotenv()
URL = os.getenv("API_URL")

def fetch_market_data():
    logger.info(f"Attempting to fetch data from {URL[:30]}...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        logger.info("Successfully retrieved API payload.")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch data: {str(e)}") # Log as ERROR level
        return None

def save_to_bronze(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/market_data_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Bronze layer updated: {filename}")
    except IOError as e:
        logger.critical(f"Disk write failed: {e}")

if __name__ == "__main__":
    logger.info("Starting Ingestion Pipeline...")
    raw_data = fetch_market_data()
    
    if raw_data:
        save_to_bronze(raw_data)
    else:
        logger.warning("Pipeline finished with no data ingested.")