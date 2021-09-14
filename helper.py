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
        df = pd.read_csv(file, encoding="latin-1", header=None)
        Helper.printline(f"Rows in file {file}: {df.shape[0]}")
        df.drop_duplicates(keep='first', inplace=True)
        Helper.printline(f"Rows in file {file} after duplicates removed: {df.shape[0]}")
        df.to_csv(file, header=False, index=False)
        
    # This helper method is useful to get a list of the folders only and ignore any files
    def list_folders():
        return [x for x in os.listdir() if os.path.isdir(x)]

    def list_country_folders():
        country_folders = Helper.list_folders()
        country_folders.remove("no_country")
        return country_folders

    def get_perc(count, total):
        if total == 0:
            return 0
            
        return round((float(count) / float(total)) * 100, 2)
    
    def remove_non_ascii_characters(string_unicode):
        string_encode = string_unicode.encode("ascii", "ignore")
        string_decode = string_encode.decode()
        return string_decode