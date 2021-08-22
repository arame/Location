import csv, os
import pandas as pd
from config import Hyper
from user_location import UserLocation
from helper import Helper
from sentiment import Sentiment

def main():
    Helper.printline("** Location Started\n")
    if Hyper.is_country:
        calculate_country_from_User_Location()
    if Hyper.is_sentiment:
        calculate_sentiment()
    Helper.printline("\n** Location Ended")

def calculate_country_from_User_Location():
    Helper.printline("     ** Started: Calculate country from User Location")
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
    Helper.printline(f"     ** Ended: Calculate country from User Location")

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

#==========================================================================================================
def calculate_sentiment():
    # Create the sentiment columns on the tweet files
    # See https://stackoverflow.com/questions/11070527/how-to-add-a-new-column-to-a-csv-file
    curr_dir = os.getcwd()
    Helper.printline("   Started Sentiment calculation")
    Helper.printline(f"Current directory: {curr_dir}")
    dir = Hyper.HyrdatedTweetLangDir
    os.chdir(dir)
    Helper.printline(f"Changed directory to {dir}")
    list_dirs = Helper.list_country_folders()
    sent = Sentiment()
    i = 0
    Helper.printline(f"Iterate through {len(list_dirs)} countries")
    for country in list_dirs:
        i += 1
        country_dir = get_country_dir(i, country)
        os.chdir(country_dir)
        csv_input = pd.read_csv(Hyper.HyrdatedTweetFile, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
        csv_input = csv_input.drop_duplicates()     # remove duplicate tweets
        sent.get(csv_input)
        insert_new_columns(csv_input)
        csv_input.query(f'sentiment != {sent.NEUTRAL}', inplace = True)
        save_csv(csv_input, sent, Hyper.HyrdatedTweetFile)
        Helper.printline(f"Country: {i}. {country} saving {len(csv_input)} entries")
        facemask_perc = Helper.get_perc(sum(sent.is_facemask), len(csv_input))
        Helper.printline(f"Number of facemask comments are {sum(sent.is_facemask)}, {facemask_perc}%")
        lockdown_perc = Helper.get_perc(sum(sent.is_lockdown), len(csv_input))
        Helper.printline(f"Number of lockdown comments are {sum(sent.is_lockdown)}, {lockdown_perc}%")
    
    Helper.printline("    Finished Sentiment calculation")

def insert_new_columns(csv_input):
    insert_column(csv_input, "is_lockdown", False)
    insert_column(csv_input, "is_facemask", False)
    insert_column(csv_input, "sentiment", 0)
    insert_column(csv_input, "s_compound", 0.0)
    insert_column(csv_input, "s_neg", 0.0)
    insert_column(csv_input, "s_neu", 0.0)
    insert_column(csv_input, "s_pos", 0.0)

def insert_column(csv_input, col_name, _default):
    column_position = 7
    column_title = col_name
    csv_input.insert(column_position, column_title, _default)

def save_csv(csv_input, sent, file):
    #df = DataFrame()
    csv_input["clean_text"] = sent.clean_text
    csv_input["s_pos"] = sent.pos
    csv_input["s_neu"] = sent.neu
    csv_input["s_neg"] = sent.neg
    csv_input["s_compound"] = sent.com
    csv_input["sentiment"] = sent.sent
    csv_input["is_facemask"] = sent.is_facemask
    csv_input["is_lockdown"] = sent.is_lockdown
    csv_input.to_csv(file) 
    
def get_country_dir(i, country):
    if i == 1:
        return country
    
    return f"../{country}"

if __name__ == "__main__":
    main()