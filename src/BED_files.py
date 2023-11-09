'''############################################################################
BED file feature
############################################################################'''

import requests
import json

# Create class for requests
class MyRequests:

    def __init__(self):
        self.base_url = "https://grch37.rest.ensembl.org"
        # Update the URL to include the correct version and endpoint
        self.url = "/lookup/symbol/homo_sapiens/BRCA2?" #BRCA2

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url, headers={ "Content-Type" : "application/json"})

 # Create an instance of MyRequests
my_requests = MyRequests()

# Make the API request
response = my_requests.request_data()

#print the output
print("Reference genome:", response.json()["assembly_name"])
print("Cannonical transcript:", response.json()["canonical_transcript"])
print("Start coordinate:", response.json()["start"])
print("End coordinate:", response.json()["end"])