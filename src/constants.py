SMA_LOW = 2
SMA_HIGH = 22
ALLOWABLE_MARGIN = 57

report = {
    "buy":{
        "time":0,"price":0
    },
    "sell":{
        "time":0,"price":0
    },
    "profit": 0
}

CSV_3600 = "../csv/data_3600.csv"
CSV_36000 = "../csv/data_36000.csv"
CSV_ALL = "../csv/data_all.csv"
CSV_FILES = [CSV_3600, CSV_36000, CSV_ALL]