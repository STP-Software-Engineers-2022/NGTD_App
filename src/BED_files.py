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
        self.gene = gene
        self.ref_genome = reference_genome
        self.base_url = "https://rest.variantvalidator.org/"
        # Update the URL to include the correct version and endpoint
        self.url = "".join(["/VariantValidator/tools/gene2transcripts_v2/", 
                            gene, "/mane/all/", reference_genome])

    # Method that makes the call to the API using the get method
    def get_response(self):
        return requests.get(self.base_url + self.url, 
                            headers={"Content-Type": "application/json"})
    
    def save_bed_file(self, response):

        output_file = f"output/{self.gene}_{self.ref_genome}.bed"
        transcript = response.json()

        chromosome = transcript[0]["transcripts"][0]["annotations"]\
            ["chromosome"]
        gene_symbol = transcript[0]["current_symbol"]
        hgnc = transcript[0]["hgnc"]
        transcript_id = transcript[0]["transcripts"][0]["reference"]

        with open(output_file, "w") as file:
            file.write(f"#GENE symbol: {gene_symbol}\n")
            file.write(f"#HGNC synbol: {hgnc}\n")
            file.write(f"#REFERENCE GENOME BUILD: {self.ref_genome}\n")
            file.write(f"#TRANSCRIPT: {transcript_id}\n")
            file.write(f"#CHROMO\t #EXON\t #START\t #END\n")

            for genomic_span_key, genomic_span_value in transcript[0]\
                ["transcripts"][0]["genomic_spans"].items():
                for exon in genomic_span_value["exon_structure"]:
                    exon_number = exon["exon_number"]
                    start = exon["genomic_start"]
                    end = exon["genomic_end"]
                    file.write('\t'.join(["chr" + str(chromosome),
                        str(exon_number), str(start - 30), str(end + 10), "\n"
                    ]))



def main():
    # Get command line arguments
    args = cli_obj(sys.argv[1:]).args

    # Create an instance of request_data
    request_obj = request_data(args.gene, args.reference_genome)
    response = request_obj.get_response()


    if args.bed_file:  # Check if the -b flag is present to create bed file
         request_obj.save_bed_file(response)
        

if __name__ == "__main__":
    main()