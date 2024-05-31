"""ctrlX class module"""
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
        metadata = self.get_data(f"automation/api/v2/nodes/{url}?type=metadata")
        if metadata.status_code == 200:
            if metadata.json()["value"]["operations"]["read"] == True:
                value = self.get_data(f"automation/api/v2/nodes/{url}")
                if value.status_code == 200:
                    if value.json()["type"] != "string" or metadata.json()["value"]["operations"]["browse"] == False:
                        return value.json()
            if metadata.json()["value"]["operations"]["browse"] == True:
                sub_items = self.get_data(f"automation/api/v2/nodes/{url}?type=browse")
                item_values = {}
                if sub_items.status_code == 200:
                    for sub_item in sub_items.json()["value"]:
                        item_value = self.get_folder(f"{url}/{sub_item}")
                        item_values[sub_item] = item_value
                if len(item_values) > 0:
                    return item_values
            return {}

    def put_data(self, url, data):
        """Use PUT to write data to the ctrlX"""
        return self.client.put(f"{self.url}/{url}", headers=self.token, json=data)

    def put_folder(self, path, data):
        """
        If data is a list of values, write them, if it is a folder call the
        put_folder method on it
        """
        for datum in data:
            if "value" in data[datum]:
                response = self.put_data(f"automation/api/v2/nodes/{path}/{datum}", data[datum])
                print(f"{path}/{datum}, {response}")
            else:
                self.put_folder(f"{path}/{datum}", data[datum])
