import time, os
import pandas as pd

class Helper:
    def printline(text):
        _date_time = time.strftime('%Y/%m/%d %H:%M:%S')
        print(f"{_date_time}   {text}")

    # This helper method is useful to get a list of the folders only and ignore any files
    def listfolders():
        return [x for x in os.listdir() if os.path.isdir(x)]
    
    def remove_duplicates(file):
        df = pd.read_csv(file, encoding="latin-1", header = None)
        df.drop_duplicates(keep='first', inplace=True)
        df.to_csv(file)