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
    
    def print_info(self, response, r_code):
        # Method of printing JSON structures in a more legible format
        #json_str = json.dumps(response.json(), indent=4)
        #print(json_str)

        gene_list = []

        for gene_number in range(len(response.json()["genes"])):
            gene_symbol = response.json()["genes"][gene_number]["gene_data"]["gene_symbol"]
            gene_list.append(gene_symbol)

        # Print results to terminal screen
        print("\n")
        print("Clinical Indication:", response.json()["name"])
        print(" ".join(["Genes included in the", r_code, "panel:", " ".join(gene_list)]))
        print("\n")
