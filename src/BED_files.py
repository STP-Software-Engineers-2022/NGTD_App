'''############################################################################
BED file feature
############################################################################'''

import requests
import argparse
import sys

class cli_obj():

    def __init__(self, sys_args):
        parser = argparse.ArgumentParser(description='')

        parser.add_argument(
            '-g', '--gene', required = True, 
            help = 'Enter a gene name')
        parser.add_argument(
            '-r', '--reference_genome', required = True, 
            help = 'GRCh37 or GRCh38?')
        parser.add_argument(
            '-b', '--bed_file', action='store_true', 
            help = 'Generates a seperate bed file')
        
        self.args = parser.parse_args(sys_args)

# Create class for requests
class request_data():

    def __init__(self, gene, reference_genome):
        self.base_url = "https://rest.variantvalidator.org/"
        # Update the URL to include the correct version and endpoint
        self.url = "".join(["/VariantValidator/tools/gene2transcripts_v2/", 
                            gene, "/mane/all/", reference_genome])

    # Method that makes the call to the API using the get method
    def get_response(self):
        return requests.get(self.base_url + self.url, 
                            headers={"Content-Type": "application/json"})
    
    def save_bed_file(self, response, args):

        output_file = f"output/{args.gene}_{args.reference_genome}.bed"
        transcript = response.json()
        print(transcript)

        chromosome = transcript[0]["transcripts"][0]["annotations"]\
            ["chromosome"]
        gene_symbol = transcript[0]["current_symbol"]
        hgnc = transcript[0]["hgnc"]

        with open(output_file, "a") as file:
            sys.stdout = file
            for genomic_span_key, genomic_span_value in transcript[0]\
                ["transcripts"][0]["genomic_spans"].items():
                for exon in genomic_span_value["exon_structure"]:
                    exon_number = exon["exon_number"]
                    start = exon["genomic_start"]
                    end = exon["genomic_end"]

                    print('\t'.join([
                        str(args.reference_genome),
                        "chr" + str(chromosome),
                        str(gene_symbol),
                        str(hgnc),
                        str(exon_number),
                        # vv  includes 30 bases upstream of exon start
                        str(start - 30),
                        # vv  includes 10 bases downstream of exon end
                        str(end + 10)
                        ]))
            sys.stdout = sys.__stdout__


def main():
    # Get command line arguments
    args = cli_obj(sys.argv[1:]).args

    # Create an instance of request_data
    request_obj = request_data(args.gene, args.reference_genome)
    response = request_obj.get_response()


    if args.bed_file:  # Check if the -b flag is present to create bed file
         request_obj.save_bed_file(response, args)
        


if __name__ == "__main__":
    main()