from main import remove_neutral_sentment_per_country
from config import Hyper
from helper import Helper
import os

def test3():
    Helper.printline("** Started")
    file = os.path.join("../_en", Hyper.HyrdatedTweetFile)
    remove_neutral_sentment_per_country("UK", file)
    Helper.printline("** Ended")
    
if __name__ == "__main__":
    test3()