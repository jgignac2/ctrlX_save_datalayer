"""
This program reads all datalayer nodes in the selected path and saves them 
as a json file
"""
import json
import datetime
import httpx

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


class CtrlX:
    """ctrlX class"""

    def __init__(self, client, url, username, password):
        """
        The initial method passes the httpx client, and connection info, then
        create the connection by getting the token.
        """
        self.client = client
        token_url = f"{url}/identity-manager/api/v2/auth/token?dryrun=false"
        payload = {"name": username, "password": password}
        token = self.client.post(token_url, json=payload)
        self.token = {"Authorization": "Bearer " + token.json()["access_token"]}
        self.url = url

    def get_data(self, url):
        """Do a GET using the token to read data"""
        return self.client.get(f"{self.url}/{url}", headers=self.token)

    def get_folder(self, url):
        """
        Read the folder contents, if it is a variable return the variable.
        If it is a folder call the get_folder method to get its values.
        This method is recursive.
        """
        folder = self.get_data(f"automation/api/v2/nodes/{url}")
        if folder.status_code in (404, 501):
            sub_items = self.get_data(f"automation/api/v2/nodes/{url}?type=browse")
            item_values = {}
            for sub_item in sub_items.json()["value"]:
                item_value = self.get_folder(f"{url}/{sub_item}")
                item_values[sub_item] = item_value
            return item_values

        return folder.json()


if __name__ == "__main__":
    main()
