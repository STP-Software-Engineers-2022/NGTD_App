import requests

# Create class for requests
class MyRequests:

    def __init__(self, myR_Number):
        self.base_url = "https://panelapp.genomicsengland.co.uk/api/v1"
        # Update the URL to include the correct version and endpoint
        self.url = "".join(["/panels/", myR_Number]) #R334

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url)
