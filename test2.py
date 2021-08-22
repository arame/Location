from helper import Helper
from config import Hyper

def test2():
    Helper.printline("** Started")
    Helper.remove_duplicates(Hyper.UserLocationFile)
    Helper.printline("** Ended")
    
if __name__ == "__main__":
    test2()