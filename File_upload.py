import os
import json
import pandas as pd
from functions import *
import time
import shutil
import psycopg2
from sqlalchemy import create_engine

def get_insert_recs(df,s):

    readings_values = df[["timestamp","value"]]
    minReadingTime = df['timestamp'].min()
    maxReadingTime = df['timestamp'].max()
    unit = unit_lookup.loc[unit_lookup["sensor"] == s, "unit"].iloc[0]
    
    
    readings_values = df[["timestamp","value"]]
    json_output = readings_values.to_json(orient='records')

    avg_reading = df["value"].mean()
    cnt_reading = df["value"].count()
    min_reading = df["value"].min()
    max_reading = df["value"].max()
    std_reading = df["value"].std()

    record_json= pd.DataFrame(columns = ["startTimestamp","sensorId", "unit", "valuesJson"])
    record_json.loc[0] = [minReadingTime,s,unit,json_output]

    record_agg= pd.DataFrame(columns = ["StartTimestamp",'EndTimestamp', "SensorId","AvgValue","MaxValue","MinValue","StandardDev", "Unit", "ValueCount"])
    record_agg.loc[0] = [minReadingTime,maxReadingTime,s,avg_reading,max_reading,min_reading,std_reading,unit,cnt_reading]

    return record_agg, record_json


def insert_recs(record_agg_row, record_json_row):
    record_agg_row.to_sql("Garden", engine, if_exists='append', index=False)
    record_json_row.to_sql("Garden Json", engine, if_exists='append', index=False)

def utc_to_timestamp(utc):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utc))

# Specify the directory containing the JSON files
json_directory = r'/home/samwise/actions/actions-runner/server/Garden/Garden/data/closed_jsons'

db_connection_str = 'postgresql+psycopg2://samwise:1420SR@localhost:5432/gardendev'
engine = create_engine(db_connection_str)


unit_lookup = pd.DataFrame(columns = ["sensor", "unit"])


unit_lookup.loc[len(unit_lookup)] = ["humidity","% rH" ]
unit_lookup.loc[len(unit_lookup)] = ["temperature","deg C" ]
# List all JSON files in the directory
json_files = [file for file in os.listdir(json_directory) if file.endswith('.json')]

# Initialize an empty list to store DataFrames
dataframes = []

# Iterate through the JSON files and load data
for file in json_files:
    file_path = os.path.join(json_directory, file)
    with open(file_path, 'r') as f:
        data = json.load(f)
        # Convert JSON data to DataFrame
        df = pd.json_normalize(data)

        if len(df) == 0:
            shutil.move(file_path, r'/home/samwise/actions/actions-runner/server/Garden/Garden/data/closed_jsons/sent_to _sql')
            print("moved ", file_path)
            continue
        df["timestamp"] = df["time"].apply(utc_to_timestamp)

        sensors = set(df["sensor"])

        for s in sensors.__iter__():
            readings = df[df['sensor'] == s]

            record_agg_row, record_json_row = get_insert_recs(readings,s)
            insert_recs(record_agg_row, record_json_row)
    shutil.move(file_path, r'/home/samwise/actions/actions-runner/server/Garden/Garden/data/closed_jsons/sent_to _sql')
    print("moved ", file_path)
    
    



        



# Display the resulting DataFrame

