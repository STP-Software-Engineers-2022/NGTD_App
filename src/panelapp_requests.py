import requests

class MyRequests:

    def __init__(self, myR_Number):
        self.base_url = "https://panelapp.genomicsengland.co.uk/api/v1"
        self.url = "".join(["/panels/", myR_Number])

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url)
    
    def gene_list(self, response):
        gene_list = []
        for gene_number in range(len(response.json()["genes"])):
            gene_symbol = response.json()["genes"][gene_number]\
                                        ["gene_data"]["gene_symbol"]
            gene_list.append(gene_symbol)

        return gene_list

    def print_info(self, response, r_code, gene_list):
        # Print results to terminal screen
        print("\n")
        print("Clinical Indication:", response.json()["name"])
        print(" ".join(
            ["Genes included in the", r_code, 
             "panel:", " ".join(gene_list)]))
        print("\n")