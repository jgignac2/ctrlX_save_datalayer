"""This program reads all datalayer nodes in the selected path"""
import json
import httpx

URL = "https://192.168.0.5"
PATH = "plc/app/Application/sym"
USERNAME = "jpg"
PASSWORD = "jpg"


def main():
    """Run the get_folder method on the selected path"""
    with httpx.Client(verify=False) as client:
        ctrlx = CtrlX(client, URL, USERNAME, PASSWORD)
        data = ctrlx.get_folder(PATH)
        json_text = json.dumps(data, indent=4, sort_keys=True)

        print(json_text)


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