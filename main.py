import csv, os
import pandas as pd
from config import Hyper
from user_location import UserLocation
from helper import Helper

def main():
    Helper.printline("     ** Started: Caculate country from User Location")
    file = os.path.join(Hyper.HyrdatedTweetDirNoCountry, Hyper.HyrdatedTweetFile)
    Helper.remove_duplicates(Hyper.UserLocationFile)
    i = 0
    ul = UserLocation()
    with open(file, encoding="utf-8", newline='') as csvfile:
        Helper.printline(f"     {file} opened")
        reader = csv.DictReader(csvfile)
        for row in reader:
            i += 1
            output_row(ul, row)
            if i % 100 == 0:
                Helper.printline(f"     {i} rows processed")

    Helper.remove_duplicates(Hyper.UserLocationFile)
    Helper.printline(f"     ** Ended: Caculate country from User Location")

def output_row(ul, row):
    user_location = row["User Location"].strip()
    if len(user_location) < 2:
        return  # Ignore, no country to save

    if user_location.lower() == "sheher" or user_location.lower() == "worldwide":
        return # ignore invalid user locations

    country = ul.locator(user_location)
    if len(country) == 0:
        return  # Ignore, no country to save

    row["Country"] = country
    save_dir = os.path.join(Hyper.HyrdatedTweetLangDir, country)
    ul.save_to_country_file(save_dir, row)

if __name__ == "__main__":
    main()