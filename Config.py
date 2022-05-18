from pathlib import Path

class Config():
    """
    This class holds constants along the project like numbers and paths
    Tutorial on pathlib: https://realpython.com/python-pathlib/
    """
    ORIGINAL_DATASET_DIR_PATH = Path("./originalDataset")
    ATHLETES_FILE_PATH = ORIGINAL_DATASET_DIR_PATH / "athlete_events.csv"
    REGIONS_FILE_PATH = ORIGINAL_DATASET_DIR_PATH / "noc_regions.csv"
    CLEANED_DATASET_DIR_PATH = Path("./cleanedDataSet")
    CLEANED_ATHLETES_FILE_PATH = CLEANED_DATASET_DIR_PATH / "cleaned_athlete_events.csv" 
    CLEANED_REGIONS_FILE_PATH = CLEANED_DATASET_DIR_PATH / "noc_regions.csv"