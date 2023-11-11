'''####################################################################
Purpose: For making requests to panelapp api, packaging data for  
database deposition
Date: 07/11/2023
####################################################################'''
import requests

# Create class for requests
class MyRequests:

    def __init__(self, r_code):
        self.base_url = "https://panelapp.genomicsengland.co.uk/api/v1"
        # Update the URL to include the correct version and endpoint
        self.url = "".join(["/panels/", r_code])

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url)
    
    # Method that prints key data to the terminal
    def print_info(self, response, r_code):
        g_list = [g["gene_data"]["gene_symbol"] \
            for g in response.json()["genes"]]

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
        print(" ".join(["\nGenes included in the", r_code, "panel:", \
            " ".join(g_list), "\n"]))
    
    # Method that packages data in dictionary ready for database & checks if user is okay with non-GMS signed panels
    def database_postage(self, response, r_code, bed):
        # bed is a boolean variable for whether the user wants a bed or not 
        if bed:
            # Get gene symbols and HGNC IDs in lists for dictionary    
            g_list = [g["gene_data"]["gene_symbol"] \
            for g in response.json()["genes"]]

            h_list = [g["gene_data"]["hgnc_id"] \
                for g in response.json()["genes"]]

            # Get GMS signed off status, checking whether a record exists or not
            try:
                signoff = response.json()["types"][2]["name"]
            except:
                signoff = "not GMS signed-off"

            if signoff == "not GMS signed-off":
                # Ask user for input
                user_input = input("Do you want to continue with the analysis?\
                    (yes/no): ").lower()

                if user_input == "yes":
                    # Initiate dictionary for R number
                    r_dict = {}

                    r_dict = {"r_number": r_code, "signoff_status": signoff, \
                        "genes": g_list, "hgnc_id_list": h_list}
                    print(r_dict)
                    return r_dict
                else:
                    print(" ".join(["\nAnalysis ended due to", r_code, "not being GMS signed off."]))
                    
        