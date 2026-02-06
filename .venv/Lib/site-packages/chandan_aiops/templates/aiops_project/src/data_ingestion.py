import pandas as pd
from src.logger import get_logger
from config import Config

logger = get_logger(__name__)

def ingest_data():
    logger.info("Data ingestion started")

    df = pd.read_csv(Config.RAW_DATA_PATH)

    logger.info(f"Data loaded with shape {df.shape}")
    logger.info("Data ingestion completed")

    return df