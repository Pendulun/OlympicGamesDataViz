from pathlib import Path

class Config():
    """
    This class holds constants along the project like numbers and paths
    Tutorial on pathlib: https://realpython.com/python-pathlib/
    """
    ORIGINAL_DATASET_DIR_NAME = 'originalDataset'
    ATHLETES_FILE_NAME = "athlete_events.csv"
    REGIONS_FILE_NAME = "noc_regions.csv"
    CLEANED_DATASET_DIR_NAME = 'cleanedDataSet'
    CLEANED_ATHLETES_FILE_NAME = "cleaned_athlete_events.csv" 
    CLEANED_REGIONS_FILE_NAME = "cleaned_noc_regions.csv"
    CLEANED_NOC_COUNTRY_CONTINENT = "NOC_Country_Continent_Cleaned.csv"
    YEAR_COUNTRY_HOST = "yearCountryHost.csv"