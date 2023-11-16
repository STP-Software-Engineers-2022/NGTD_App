""" Makes a request for a gene list from a given R number"""
import requests
import sys
from config import log

class MyRequests:
    """
    Object that initialises with a URL to make the request
    
    Attributes
    __________
    base_url : str
        a static base URL to be appended to in later requests
    url : str
        the url appendage that contains the r_number passed into from args

    Methods
    _______
    request_data()
        performs the API request
    gene_list(response)
        generates the list of genes from the gene panel from the API response
    print_info(response, r_code, gene_list)
        prints the gene list to the terminal along with clinical indication
    """

    def __init__(self, r_number):
        self.base_url = "https://panelapp.genomicsengland.co.uk/api/v1"
        self.url = "".join(["/panels/", r_number])

    def request_data(self):
        try:
            response = requests.get(
                self.base_url + self.url, timeout=2, verify=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print('HTTP Error: R number is not associated with a gene panel '
                  'or does not exist.\nPlease refer to Genomic Test Directory'
                  ' for guidance.')
            log.error(errh.args[0])
            sys.exit(1)
        except requests.exceptions.ReadTimeout as errt:
            print("Error: Time out on API request")
            log.error(errt.args[0])
            sys.exit(1)
        except requests.exceptions.ConnectionError as conerr:
            print("Connection Error: No internet connection")
            log.error(conerr.args[0])
            sys.exit(1)

        return response
    
    def gene_list(self, response):
        gene_list = []
        try:
            for gene_number in range(len(response.json()["genes"])):
                gene_symbol = response.json()["genes"][gene_number]\
                                            ["gene_data"]["gene_symbol"]
                gene_list.append(gene_symbol)
        except KeyError as kerr:
            print("Error: incorrect format of API response."
                  f"{kerr} field not present in JSON.")
            log.critical(kerr)
            quit()

        return gene_list

    def print_info(self, response, r_code, gene_list):
        print("\nClinical Indication:", response.json()["name"])
        print(" ".join(
            ["Genes included in the", r_code, 
             "panel:", " ".join(gene_list)]))