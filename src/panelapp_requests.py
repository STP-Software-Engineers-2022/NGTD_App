"""
This modules provides a class for handling API requests related to 
the Genomics England PanelApp.

Example usage:
    my_requests = MyRequests(args)
    response = my_requests.request_data()
    gene_list, signoff = my_requests.gene_list(response)
    my_requests.print_info(response, my_requests.r_code, gene_list, signoff)
    panel_info = my_requests.database_postage(response)

Authors: D. Ajayi, N. Gallop
"""
import requests
import sys
from config import log

class MyRequests:
    """
    MyRequests is a class which deals with API requests and uses data for a   
    given R number.

    This class makes requests to the Genomics England PanelApp API,
    obtaining gene panel data using an R number provided by the user. 
    It allows for extracting gene lists, printing panel information, and 
    preparing data for database insertion.

    Attributes
    ----------
    r_code : str
        The R number provided by the user, used to query the Genomics England
        API.
    create_bed : boolean
        A flag indicating whether a BED file should be created from the 
        retrieved gene data.
    base_url : str
        The base URL of the Genomics England PanelApp API.
    url : str
        The full URL constructed for API requests, including the R number.    

    Methods
    -------
    request_data()
        Performs an API request to retrieve gene panel data based on the 
        R number.
        Returns a response object data from the API.

    gene_list(response)
        Extracts and returns a list of gene symbols from the API response, 
        along with the panel's GMS sign-off status.

    print_info(response, r_code, gene_list, signoff)
        Prints detailed panel information, including clinical indication and 
        gene list.

    database_postage(response)
        Prepares and returns a dictionary of data extracted from the API 
        response to input into database. 
        Prompts the user for confirmation if the panel is not GMS signed-off.

    Raises
    ------
    HTTPError, ReadTimeout, ConnectionError
        Handles various exceptions related to API requests.

    Dependencies
    ------------
    - requests: Required for performing API requests.
    - logging: Used for logging errors and critical issues.

    Example
    -------
    my_requests = MyRequests(args)
    response = my_requests.request_data()
    gene_list, signoff = my_requests.gene_list(response)
    my_requests.print_info(response, my_requests.r_code, gene_list, signoff)
    data_for_db = my_requests.database_postage(response)
    """

    def __init__(self, args):
        try:
            self.r_code = args.r_number
            self.url = "".join(["/panels/", self.r_code])
        except TypeError:
            raise ValueError("Enter an R number using the '-r' flag it should be a string. e.g. R134")
        self.create_bed = args.create_bed
        self.base_url = "https://panelapp.genomicsengland.co.uk/api/v1"
        
    

    def request_data(self):
        """
        Perform an API request to retrieve gene panel data.

        This method sends a GET request to the URL and handles a number of 
        exceptions related to the request. The response object is returned if  
        the request works out.

        Returns
        -------
        response : requests.Response
            The response object from the API request.

        Raises
        ------
        HTTPError
            If the R number is not associated with a gene panel or does 
            not exist.
        ReadTimeout
            If there is a timeout while making the API request.
        ConnectionError
            If there is a connection error during the request.
        """
        try:
            response = requests.get(
                self.base_url + self.url, timeout=20, verify=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error: R number is not associated with a gene panel "
                  "or does not exist.\nPlease refer to Genomic Test Directory"
                  " for guidance.")
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
        """
        Extract and return the list of gene symbols from the API response.

        Alongside the gene list, this method determines the GMS sign-off
        status of the panel and returns it.

        Parameters
        ----------
        response : requests.Response
            The response object from the API request.

        Returns
        -------
        tuple
            A tuple containing the list of gene symbols and the GMS sign-off 
            status.

        Raises
        ------
        KeyError
            If the expected fields are not present in the API response.
        """
        gene_list = []
        try:
            gene_list = [gene["gene_data"]["gene_symbol"] \
                for gene in response.json()["genes"]]
        except KeyError as kerr:
            print("Error: incorrect format of API response."
                  f"{kerr} field not present in JSON.")
            log.critical(kerr)
            sys.exit(1)
            
        # Get GMS signed off status
        panel_info = [status["name"] for status in response.json()["types"]]

        if "GMS signed-off" in panel_info:
            signoff = "GMS signed-off"
        else:
            signoff = "not GMS signed-off"

        return gene_list, signoff

    def print_info(self, response, r_code, gene_list, signoff):
        """
        Print detailed information about the gene panel.

        This includes the sign-off status, clinical indication, and the list
        of genes included in the panel.

        Parameters
        ----------
        response : requests.Response
            The response object from the API request.
        r_code : str
            The R number associated with the gene panel.
        gene_list : list
            List of genes included in the panel.
        signoff : str
            The GMS sign-off status of the panel.
        """
        print("\nThis panel is", signoff)
        print("\nClinical Indication:", response.json()["name"])
        print(" ".join(
            ["Genes included in the", self.r_code, 
             "panel:", " ".join(gene_list)]))

    def database_postage(self, response):
        """
        Prepare and return data for database insertion.

        This method packages the data from the API response into a dictionary.
        If the panel is not GMS signed-off, it prompts the user for 
        confirmation before proceeding.

        Parameters
        ----------
        response : requests.Response
            The response object from the API request.

        Returns
        -------
        Dictionary or None
            A dictionary containing the packaged data for database insertion,
            or None if the user opts not to proceed with non-GMS signed-off 
            panels.

        Notes
        -----
        The user is prompted for confirmation if the panel is not GMS 
        signed-off.
        """
        r_code = self.r_code
        bed = self.create_bed

        # bed is a boolean variable for whether the user wants a bed or not 
        if bed:
            # Get gene symbols & HGNC IDs in lists as well as panel id for 
            # dictionary    
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
                user_input = input("Do you want to continue with the \
                    analysis? (yes/no): ").lower()

                if user_input == "yes":

                    r_dict = {"r_number": r_code, "panel_id": panel_id, \
                        "panel_version": p_version, "signoff_status":  \
                        signoff, "genes": g_list, "hgnc_id_list": h_list}

                    print(r_dict) # for checking todelete
                    return r_dict
                else:
                    print(" ".join(["\nAnalysis ended due to", r_code, 
                                    "not being GMS signed off."]))
            elif signoff == "GMS signed-off":
                r_dict = {"r_number": r_code, "panel_id": panel_id, \
                    "panel_version": p_version, "signoff_status": signoff, \
                    "genes": g_list, "hgnc_id_list": h_list}
                return r_dict
                