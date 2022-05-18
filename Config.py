from pathlib import Path

class Config():
    ORIGINAL_DATASET_DIR_PATH = Path("./originalDataset")
    ATHLETES_FILE_PATH = ORIGINAL_DATASET_DIR_PATH / "athlete_events.csv"
    REGIONS_FILE_PATH = ORIGINAL_DATASET_DIR_PATH / "noc_regions.csv"
    CLEANED_DATASET_DIR_PATH = Path("./cleanedDataSet")
    CLEANED_ATHLETES_FILE_PATH = CLEANED_DATASET_DIR_PATH / "cleaned_athlete_events.csv" 
    CLEANED_REGIONS_FILE_PATH = CLEANED_DATASET_DIR_PATH / "noc_regions.csv"