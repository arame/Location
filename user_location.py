from helper import Helper
from geopy.geocoders import Nominatim
import csv, os, re
import pandas as pd
from csv import writer
from csv import DictWriter
from config import Hyper

class UserLocation:
    def __init__(self) -> None:
        # initialize geolocator
        self.geolocator = Nominatim(user_agent='Tweet_locator')
        self.user_locations ={}
        reader = csv.reader(open(Hyper.UserLocationFile, encoding='utf-8', errors="ignore"))
        for row in reader:
            key = row[0]
            self.user_locations[key] = row[1]
            
    def save_user_location(self, user_location, country):
        self.user_locations[user_location] = country
        # Open file in append mode
        with open(Hyper.UserLocationFile, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            try:
                csv_writer.writerow([user_location, country])
            except:
                pass
            
    def locator(self, user_location):
        if user_location == None:
            return ""

        temp = re.sub("[^a-zA-Z]+", "", user_location)
        if len(temp) < 2:
            return ""
        
        if "#name" in user_location.lower():
            return ""
        
        if "#value" in user_location.lower():
            return ""
        
        if "n/a" in user_location.lower():
            return ""
        
        if " null " in user_location.lower():
            return ""
        
        if " false " in user_location.lower():
            return ""
        
        get_country = lambda country: "" if len(country) > 50 else country
        if user_location in self.user_locations:
            country = self.user_locations[user_location]
            return get_country(country)

        country = self.geo_locator(user_location)
        self.save_user_location(user_location, country)
        return get_country(country)

    def geo_locator(self, user_location):
        try :
            # get location
            location = self.geolocator.geocode(user_location, language='en')
            # get coordinates
            location_exact = self.geolocator.reverse(
                        [location.latitude, location.longitude], language='en')
            # get country codes
            c_code = location_exact.raw['address']['country_code']
            country = location_exact.raw['address']['country']
            country = Helper.remove_non_ascii_characters(country)
            return country

        except:
            return ""

    def save_to_country_file(self, dir, row):
        directory_path = os.getcwd()
        self.change_working_directory(dir)
        self.append_dict_as_row(row)
        os.chdir(directory_path) 

    def append_dict_as_row(self, row):
        output_file = Hyper.HyrdatedTweetFile
        if os.path.exists(output_file):
            # Open file in append mode
            with open(output_file, 'a+', encoding="utf-8", newline='') as write_obj:
                dict_writer = DictWriter(write_obj, fieldnames=Hyper.field_names)
                dict_writer.writerow(row)
                return

        with open(output_file, 'w', encoding="utf-8", newline='') as write_obj:
            dict_writer = DictWriter(write_obj, fieldnames=Hyper.field_names)
            dict_writer.writeheader()
            dict_writer.writerow(row)


    def change_working_directory(self, folder):

        if not os.path.exists(folder):
            os.makedirs(folder)

        os.chdir(folder)