'''############################################################################
BED file feature
############################################################################'''

import requests
import json
import argparse
import sys

class cli_obj():

    def __init__(self, sys_args):
        parser = argparse.ArgumentParser(description='')

        parser.add_argument(
            '-g', '--gene', required = True, help = 'Enter a gene name')
        parser.add_argument(
            '-r', '--reference_genome', required = True, help = 'GRCh37 or GRCh38?')
        parser.add_argument(
            '-b', '--bed_file', action='store_true', help = 'Generates a seperate bed file')
        
        self.args = parser.parse_args(sys_args)

# Create class for GRCh37 reference genome
class GRCh37:

    def __init__(self, gene_name):
        self.base_url = "https://grch37.rest.ensembl.org"
        # Update the URL to include the correct version and endpoint
        self.url = "".join(["/lookup/symbol/homo_sapiens/", gene_name, "?"]) #BRCA2

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url, headers = { "Content-Type" : "application/json"})

    def print_info(self, grch37response):
        if grch37response.ok:
            print('\t'.join([
                "".join(["chr", grch37response.json()["seq_region_name"]]),
                str(grch37response.json()["start"]),
                str(grch37response.json()["end"]),
                grch37response.json()["assembly_name"],
                grch37response.json()["display_name"],
                grch37response.json()["canonical_transcript"]
    ]))
        else:
            print("Error:", grch37response.status_code)

# Create class for GRCh38 reference genome
class GRCh38:

    def __init__(self, gene_name):
        self.base_url = "https://rest.ensembl.org"
        # Update the URL to include the correct version and endpoint
        self.url = "".join(["/lookup/symbol/homo_sapiens/", gene_name, "?"]) #BRCA2

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url, headers={ "Content-Type" : "application/json"})

    def print_info(self, grch38response):
        if grch38response.ok:
            print('\t'.join([
                "".join(["chr", grch38response.json()["seq_region_name"]]),
                str(grch38response.json()["start"]),
                str(grch38response.json()["end"]),
                grch38response.json()["assembly_name"],
                grch38response.json()["display_name"],
                grch38response.json()["canonical_transcript"]
    ]))
        else:
            print("Error:", grch38response.status_code)

# Get command line arguments
args = cli_obj(sys.argv[1:]).args

# Create an instance of GRCh37 and GRCh38 
grch37 = GRCh37(args.gene)
grch38 = GRCh38(args.gene)

if args.bed_file:  # Check if the -b flag is present to create bed file

    # Open a new .bed file for each search in append mode (-a)
    # 'With' automatically close the file after writing
    with open(args.gene + ".bed", "a") as output_file:
    
        # Redirect the standard output to the .bed file
        sys.stdout = output_file

        # Make the API requests
        grch37response = grch37.request_data()
        grch38response = grch38.request_data()

        # Print the output
        if args.reference_genome == "GRCh37": 
            grch37.print_info(grch37response)
        elif args.reference_genome == "GRCh38": 
            grch38.print_info(grch38response)

        # Restore the standard output
        sys.stdout = sys.__stdout__