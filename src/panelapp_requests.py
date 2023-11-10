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
        gene_list = [gene["gene_data"]["gene_symbol"] for gene in response.json()["genes"]]

        # Get GMS signed off status, checking whether a record exists or not
        try:
            signoff = response.json()["types"][2]["name"]
        except:
            signoff = "not GMS signed-off"

        # Print results to terminal screen
        if signoff == "GMS signed-off":
            print(" ".join(["\nThis panel is", signoff]))
        else:
            print(" ".join(["\nThis panel is", signoff]))
        print("\nClinical Indication:", response.json()["name"])
        print(" ".join(["\nGenes included in the", r_code, "panel:", " ".join(gene_list), "\n"]))

    def database_postage(self, response, r_code):
        # Get gene symbols and HGNC IDs in lists for dictionary    
        gene_list = [gene["gene_data"]["gene_symbol"] for gene in response.json()["genes"]]
        hgnc_id_list = [gene["gene_data"]["hgnc_id"] for gene in response.json()["genes"]]
        r_code = r_code # Reminder

        # Get GMS signed off status, checking whether a record exists or not
        try:
            signoff = response.json()["types"][2]["name"]
        except:
            signoff = "not GMS signed-off"

        # Create dictionary for R number
        r_dict = {}

        r_dict = {'r_number': r_code, 'signoff_status': signoff, 'genes': gene_list, 'hgnc_id_list': hgnc_id_list}
        print(r_dict)
        return r_dict
        