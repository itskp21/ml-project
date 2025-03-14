import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split  # type: ignore
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionConfig:
    train_path: str = os.path.join('artifacts', 'train.csv')
    test_path: str = os.path.join('artifacts', 'test.csv')
    raw_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered the data ingestion method.')

        try:
            data_path = os.path.join('notebook', 'data', 'stud.csv')

            # Check if the dataset file exists
            if not os.path.exists(data_path):
                logging.error(f"Dataset file not found at {data_path}")
                raise FileNotFoundError(f"Dataset file not found at {data_path}")

            df = pd.read_csv(data_path)
            logging.info(f"Dataset loaded successfully with shape {df.shape}")
            logging.info(f"Dataset columns: {df.columns.tolist()}")

            # Ensure artifacts directory exists
            artifacts_dir = os.path.dirname(self.ingestion_config.train_path)
            if not os.path.exists(artifacts_dir):
                os.makedirs(artifacts_dir, exist_ok=True)
                logging.info(f"Created artifacts directory: {artifacts_dir}")

            # Save raw data
            df.to_csv(self.ingestion_config.raw_path, index=False, header=True)
            if os.path.exists(self.ingestion_config.raw_path):
                logging.info(f"Raw data saved at {self.ingestion_config.raw_path}")
            else:
                logging.error("Raw data file was not created!")

            # Edge case: dataset too small
            if df.shape[0] < 2:
                logging.error("Insufficient data for train-test split.")
                raise ValueError("Dataset needs at least 2 rows for splitting.")

            # Train-test split
            logging.info("Performing train-test split")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save train and test data
            train_set.to_csv(self.ingestion_config.train_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_path, index=False, header=True)

            if os.path.exists(self.ingestion_config.train_path) and os.path.exists(self.ingestion_config.test_path):
                logging.info("Train and Test datasets saved successfully.")
            else:
                logging.error("Train/Test CSV files were not created!")

            logging.info("Data ingestion completed successfully.")
            return self.ingestion_config.train_path, self.ingestion_config.test_path

        except Exception as e:
            import traceback
            logging.error(f"Error in Data Ingestion: {str(e)}")
            logging.error(f"Error Traceback: {traceback.format_exc()}")
            print(f"Error encountered: {e}")  # Print error for real-time debugging
            raise CustomException(e, sys)