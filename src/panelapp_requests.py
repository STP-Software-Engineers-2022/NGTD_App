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

    def __init__(self, r_code):
        self.base_url = "https://panelapp.genomicsengland.co.uk/api/v1"
        self.url = "".join(["/panels/", r_code])
    

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
        g_list = []
        try:
            g_list = [gene["gene_data"]["gene_symbol"] \
                for gene in response.json()["genes"]]
        except KeyError as kerr:
            print("Error: incorrect format of API response."
                  f"{kerr} field not present in JSON.")
            log.critical(kerr)
            sys.exit(1)
        # Get GMS signed off status
        try:
            panel_info = [status["name"] \
                for status in response.json()["types"]]
        except KeyError as kerr:
            print("Error: incorrect format of API response."
                  f"{kerr} field not present in JSON.")
            log.warning(kerr)
            sys.exit(1)
        if "GMS signed-off" in panel_info:
            signoff = "GMS signed-off"
        else:
            signoff = "not GMS signed-off"

        return g_list, signoff

    def print_info(self, response, r_code, g_list, signoff):
        print("\nThis panel is", signoff)
        try:
            print("\nClinical Indication:", response.json()["name"])
        except KeyError as kerr:
            print("Error: incorrect format of API response."
                  f"{kerr} field not present in JSON.")
            log.warning(kerr)
            sys.exit(1)
        print(f"\nGenes included in the {r_code} panel:", " ".join(g_list))


    # Method for getting panel information
    def get_panel_info(self, response):
    # Get HGNC IDs in lists as well as panel id for dictionary 
        try: 
            h_list = [g["gene_data"]["hgnc_id"] \
                    for g in response.json()["genes"]]
            panel_id = response.json()["id"]
            p_version = response.json()["version"]
            return h_list, panel_id, p_version
        except KeyError as kerr:
                print("Error: incorrect format of API response."
                    f"{kerr} field not present in JSON.")
                log.critical(kerr)
                sys.exit(1)

    # Method that packages data in dictionary ready for database & checks if user is okay with non-GMS signed panels
    def database_postage(self, response, r_code, bed, g_list, signoff):
        # bed is a boolean variable for whether the user wants a bed or not 
        if bed:
            h_list, panel_id, p_version = self.get_panel_info(response)
        else:
            h_list, panel_id, p_version = self.get_panel_info(response)

        # Initiate dictionary for R number
        r_dict = {}

            # Ask user for input in case the panel is not GMS signed
        if signoff == "not GMS signed-off":
            user_input = input("Do you want to continue with the analysis?\
                (yes/no): ").lower()
            if user_input == "yes":
                r_dict = {"r_number": r_code, "panel_id": panel_id, \
                    "panel_version": p_version, "signoff_status": signoff, \
                    "genes": g_list, "hgnc_id_list": h_list}
            else:
                print(" ".join(["\nAnalysis ended due to", r_code, "not being GMS signed off."]))
        elif signoff == "GMS signed-off":
            r_dict = {"r_number": r_code, "panel_id": panel_id, \
                "panel_version": p_version, "signoff_status": signoff, \
                "genes": g_list, "hgnc_id_list": h_list}
        try:
            print(f"\n{r_dict}")
            return r_dict
        except Exception as e:
            print(f"Dictionary for test may be missing values or empty: {e}")
            log.critical(e)
            sys.exit(1) 