'''############################################################################
Purpose: For testing objects
Date: 07/11/2023
############################################################################'''
import sys
import src.cli as cli
import argparse
import src.panelapp_requests as pan

def main():

    # initialise cli object
    cli_obj = cli.cli_obj(sys.argv[1:])
    selected_args = cli_obj.arg_selection()
    # check if arguments have been selected and abort program if not
    if selected_args == [False, False]:
        print("No arguments selected, aborting program")
        quit()
    
    r_code = cli_obj.args.r_number
    print(r_code)

    # Create an instance of MyRequests
    my_requests = pan.MyRequests(myR_Number)

    # Make the API request
    response = my_requests.request_data()

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
    print(" ".join(["Genes included in the", myR_Number, "panel:", " ".join(gene_list)]))
    print("\n")

'''
parser = argparse.ArgumentParser()

# Create flags for use
parser.add_argument("-r", "--r_number", dest = "r_number", help="e.g. -r R134")

# assigning arguments and their associated flags to a variable
args = parser.parse_args()

# Take argument parsed as variable
myR_Number = args.r_number
'''

if __name__ == "__main__":
    main()