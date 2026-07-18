import logging
import pandas as pd
from pathlib import Path
from src.config import Settings
import time

logger = logging.getLogger(__name__)

class DatasetLoader:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cache_path = Path(settings.DATA_CACHE_PATH)

    def load(self) -> pd.DataFrame:
        """Load from cache if available, otherwise download from HF."""
        start_time = time.time()
        
        if self.cache_path.exists():
            logger.info("Loading dataset from local cache")
            df = pd.read_parquet(str(self.cache_path))
            duration = int((time.time() - start_time) * 1000)
            logger.info(f"Dataset loaded: {len(df)} rows, cache_hit=True, duration={duration}ms")
            return df
            
        return self._download(start_time)

    def _download(self, start_time: float) -> pd.DataFrame:
        """Download a subset from Hugging Face directly to avoid OOM and long timeouts on Railway."""
        retries = 3
        backoff = [1, 2, 4]
        
        csv_url = f"https://huggingface.co/datasets/{self.settings.HF_DATASET_NAME}/resolve/main/zomato.csv"
        
        def usecols_filter(col_name):
            return col_name.lower() in [
                "name", "location", "city", "cuisines", "cost_for_two", 
                "approx_cost(for two people)", "rating", "rate", 
                "aggregate rating", "votes", "rest_type"
            ]
        
        for attempt in range(retries):
            try:
                logger.info(f"Streaming dataset '{self.settings.HF_DATASET_NAME}' (attempt {attempt + 1})")
                
                # Stream directly and limit to 50,000 rows to save memory and time
                df = pd.read_csv(csv_url, usecols=usecols_filter, nrows=50000)
                
                self._save_cache(df)
                
                duration = int((time.time() - start_time) * 1000)
                logger.info(f"Dataset loaded: {len(df)} rows, cache_hit=False, duration={duration}ms")
                return df
            except Exception as e:
                logger.warning(f"Download failed: {e}")
                if attempt < retries - 1:
                    time.sleep(backoff[attempt])
                else:
                    logger.error("All download attempts failed.")
                    raise Exception(f"Failed to load dataset after {retries} attempts") from e

    def _save_cache(self, df: pd.DataFrame) -> None:
        """Persist DataFrame as parquet."""
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(self.cache_path)
        logger.info(f"Dataset cached to {self.cache_path}")
