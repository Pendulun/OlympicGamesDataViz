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
    regionsDf = pd.read_csv('./'+Config.ORIGINAL_DATASET_DIR_NAME+"/"+Config.REGIONS_FILE_NAME)
    regionsDf = regionsDf.apply(createRegionForNanRegion, axis=1)

    regionsDf.to_csv('./'+Config.CLEANED_DATASET_DIR_NAME+"/"+Config.CLEANED_REGIONS_FILE_NAME, index=False)
    

def treatAthletes():
    athletesDf = pd.read_csv('./'+Config.ORIGINAL_DATASET_DIR_NAME+"/"+Config.ATHLETES_FILE_NAME)
    athletesDf['Medal'].fillna('None',inplace=True)
    #.
    #.
    #.
    athletesDf.to_csv('./'+Config.CLEANED_DATASET_DIR_NAME+"/"+Config.CLEANED_ATHLETES_FILE_NAME, index=False)

if __name__ == "__main__":
    #Config.CLEANED_DATASET_DIR_PATH.mkdir(parents=True, exist_ok=True)
    treatRegions()
    treatAthletes()