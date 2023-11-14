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
        # Update the URL to include the endpoint
        self.url = "".join(["/panels/", r_code])
        self.url_signed = "".join(["/panels/signedoff/", r_code])

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url)
    
    # Method that prints key data to the terminal
    def print_info(self, response, r_code):
        g_list = [g["gene_data"]["gene_symbol"] \
            for g in response.json()["genes"]]

        # Get GMS signed off status
        s_list = [s["name"] for s in response.json()["types"]]

        if "GMS signed-off" in s_list:
            signoff = "GMS signed-off"
        else:
            signoff = "not GMS signed-off"

        # Print results to terminal screen
        print("\nThis panel is", signoff)
        print("\nPanel ID:", response.json()["id"], \
            "".join(["v", response.json()["version"]]))

        print("\nClinical Indication:", response.json()["name"])
        print(" ".join(["\nGenes included in the", r_code, "panel:", \
            " ".join(g_list), "\n"]))


    # Method that packages data in dictionary ready for database & checks if user is okay with non-GMS signed panels
    def database_postage(self, response, r_code, bed):
        # bed is a boolean variable for whether the user wants a bed or not 
        if bed:
            # Get gene symbols & HGNC IDs in lists as well as panel id for dictionary    
            g_list = [g["gene_data"]["gene_symbol"] \
            for g in response.json()["genes"]]

            h_list = [g["gene_data"]["hgnc_id"] \
                for g in response.json()["genes"]]
            
            panel_id = response.json()["id"]
            p_version = response.json()["version"]

            # Get GMS signed off status
            s_list = [s["name"] for s in response.json()["types"]]

            if "GMS signed-off" in s_list:
                signoff = "GMS signed-off"
            else:
                signoff = "not GMS signed-off"

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

                    print(r_dict) # for checking todelete
                    return r_dict
                else:
                    print(" ".join(["\nAnalysis ended due to", r_code, "not being GMS signed off."]))
            elif signoff == "GMS signed-off":
                r_dict = {"r_number": r_code, "panel_id": panel_id, \
                    "panel_version": p_version, "signoff_status": signoff, \
                    "genes": g_list, "hgnc_id_list": h_list}
                print(r_dict)
                return r_dict
                

                    
        