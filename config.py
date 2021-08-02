import os
import time
class Hyper:
    UseUserLocation = False
    MustTranslate = False
    _time = "2021_08_01 16_16_57"
    language = "en"
    UserLocationFile = "../Lookup/UserLocations.csv"
    HyrdatedTweetDirNoCountry = f"../Summary_Details_files{_time}/{language}/no_country"
    HyrdatedTweetLangDir = f"../Summary_Details_files{_time}/{language}"
    HyrdatedTweetDir = f"../Summary_Details_files{_time}"
    HyrdatedTweetFile = "tweets.csv"
    HyrdatedTweetLangFile = f"{language}_tweets.csv"
    no_language_cnt = 0
    tweet_saved_cnt = 0
    field_names = ['Id', 'Language', 'Place', 'User Location', 'Country', 'Full Text', 'Tweet', 'English Tweet', 'Retweet Count', 'Favourite Count']
    
    def __init__(self) -> None:
        self.dirOutput = f"../Summary_Details_files{Hyper._time}"
        self.IsOutputCsv = True

 