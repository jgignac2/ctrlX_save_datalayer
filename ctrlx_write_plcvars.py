"""
This program reads a json file and write all the data in it to the ctrlx
datalayer
"""
import json
import sys
import httpx
from ctrlx import CtrlX

URL = "https://192.168.1.1"
USERNAME = "boschrexroth"
PASSWORD = "boschrexroth"


def main():
    """
    Run the get_folder method on the selected path, save to user selected
    filename when done.
    """
    filename = sys.argv[1]

    with open(filename, "r", encoding="utf-8") as file:
        file_data = json.load(file)

    with httpx.Client(verify=False) as client:
        ctrlx = CtrlX(client, URL, USERNAME, PASSWORD)
        ctrlx.put_folder("", file_data)


if __name__ == "__main__":
    main()
