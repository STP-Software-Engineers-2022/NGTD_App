'''############################################################################
BED file feature
############################################################################'''

import requests
import argparse
import json
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

# Create class for requests
class MyRequests:

    def __init__(self, gene, reference_genome):
        self.base_url = "https://rest.variantvalidator.org/"
        # Update the URL to include the correct version and endpoint
        self.url = "".join(["/VariantValidator/tools/gene2transcripts_v2/", gene, "/mane/all/", reference_genome])

    # Method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.base_url + self.url, headers={ "Content-Type" : "application/json"})

# Get command line arguments
args = cli_obj(sys.argv[1:]).args

# Create an instance of MyRequests
my_requests = MyRequests(args.gene, args.reference_genome)

if args.bed_file:  # Check if the -b flag is present to create bed file
     
     # Open a new .bed file for each search in append mode (-a)
    # 'With' automatically closes the file after writing
    with open(args.gene + "_" + args.reference_genome + ".bed", "a") as output_file:
    
        # Redirect the standard output to the .bed file
        sys.stdout = output_file

        # Make the API requests
        response = my_requests.request_data()

        # check the response status code
        if response.status_code == 200:
            
        # Print exon information
            transcripts = response.json()

            for transcript in transcripts:
                chromosome = transcript["transcripts"][0]["annotations"]["chromosome"]
                gene_symbol = transcript["current_symbol"]
                hgnc = transcript["hgnc"]

            for genomic_span_key, genomic_span_value in transcript["transcripts"][0]["genomic_spans"].items():
                for exon in genomic_span_value["exon_structure"]:
                    exon_number = exon["exon_number"]
                    start = exon["genomic_start"]
                    end = exon["genomic_end"]

                    print('\t'.join([
                        "chr" + str(chromosome),
                        str(gene_symbol),
                        str(hgnc),
                        str(exon_number),
                        str(start),
                        str(end)
                        ]))

        else:
            print("VariantValidator API request failed with status code:", response.status_code)
        
        # Restore the standard output
        sys.stdout = sys.__stdout__