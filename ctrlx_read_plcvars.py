"""
This program reads all datalayer nodes in the selected path and saves them 
as a json file
"""
import json
import datetime
import httpx
from ctrlx import CtrlX

URL = "https://192.168.1.1"
PATH = "plc/app/Application/sym"
USERNAME = "boschrexroth"
PASSWORD = "boschrexroth"


def main():
    """
    Run the get_folder method on the selected path, save to user selected
    filename when done.
    """
    with httpx.Client(verify=False) as client:
        ctrlx = CtrlX(client, URL, USERNAME, PASSWORD)
        data = {PATH: ctrlx.get_folder(PATH)}
        json_text = json.dumps(data, indent=4, sort_keys=True)

        default_filename = (
            "backup_" + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M") + ".json"
        )
        filename = input(f"Enter a filename (Leave blank for {default_filename}):")
        if filename == "":
            filename = default_filename

        with open(filename, "w", encoding="utf-8") as file:
            file.write(json_text)


if __name__ == "__main__":
    main()
