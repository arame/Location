import os
from config import Hyper
from helper import Helper

def main():
    orig_dir = os.listdir()
    list_folders = [x for x in os.listdir() if os.path.isdir(x)]
    output = []
    list_dirs = os.listdir()
    for d in list_dirs:
        if os.path.isdir(d):
            output.append(d)
    i = 0

if __name__ == "__main__":
    main()