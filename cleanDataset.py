from Config import Config
import pandas as pd


def createRegionForNanRegion(df):
    if df['NOC'] == 'ROT':
        df['region'] = 'Refugee'
    elif df['NOC'] == 'TUV':
        df['region'] = 'Tuvalu'
    elif df['NOC'] == 'UNK':
        df['region'] = 'Unknown'
    
    return df

def treatRegions():
    regionsDf = pd.read_csv(Config.REGIONS_FILE_PATH)
    regionsDf = regionsDf.apply(createRegionForNanRegion, axis=1)

    regionsDf.to_csv(Config.CLEANED_REGIONS_FILE_PATH)
    

def treatAthletes():
    athletesDf = pd.read_csv(Config.ATHLETES_FILE_PATH)

if __name__ == "__main__":
    Config.CLEANED_DATASET_DIR_PATH.mkdir(parents=True, exist_ok=True)
    treatRegions()
    #treatAthletes()