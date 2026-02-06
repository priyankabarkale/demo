"""
Configuration for AIOps Project
"""

class Config:
    PROJECT_NAME = "aiops_project"
    VERSION = "1.0.0"  # Update your version here
    
    # Paths
    DATA_RAW_PATH = "data/raw"
    DATA_PROCESSED_PATH = "data/processed"
    MODELS_PATH = "models"
    LOGS_PATH = "logs"
    RESEARCH_PATH = "research"
    
    # Model settings
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    VALIDATION_SIZE = 0.1
    
    # MLflow settings
    MLFLOW_TRACKING_URI = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME = PROJECT_NAME
    
    # API settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    DEBUG = True
    
    # DVC settings
    DVC_REMOTE = "remote_storage"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"