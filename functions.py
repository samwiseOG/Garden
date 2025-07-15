def get_insert_recs(df):

    readings_values = df[["timestamp","value"]]
    minReadingTime = df['timestamp'].min()
    maxReadingTime = df['timestamp'].max()
    unit = unit_lookup.loc[unit_lookup["sensor"] == 'humidity', "unit"].iloc[0]
    
    
    readings_values = df[["timestamp","value"]]
    json_output = readings_values.to_json(orient='records')

    avg_reading = df["value"].mean()
    cnt_reading = df["value"].count()
    min_reading = df["value"].min()
    max_reading = df["value"].max()
    std_reading = df["value"].std()

    record_json= pd.DataFrame(columns = ["startTimestamp","sensorId", "unit", "valuesJson"])
    record_json.loc[0] = [minReadingTime,"humidity","% rH",json_output]

    record_agg= pd.DataFrame(columns = ["StartTimestamp",'EndTimestamp', "SensorId","AvgValue","MaxValue","MinValue","StandardDev", "Unit", "ValueCount"])
    record_agg.loc[0] = [minReadingTime,maxReadingTime,"humidity",avg_reading,max_reading,min_reading,std_reading,"% rH",cnt_reading]

    return record_agg, record_json


def insert_recs(record_agg_row, record_json_row):
    record_agg_row.to_sql("Garden", engine, if_exists='append', index=False)
    record_json_row.to_sql("Garden Json", engine, if_exists='append', index=False)

def utc_to_timestamp(utc):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utc))