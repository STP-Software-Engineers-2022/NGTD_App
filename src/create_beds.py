'''
Generate a bed file for a gene panel
Authors: D. Scales, N. Gallop
Last updated: NG - 12/12/23
'''
from config import log
import requests
import sys


class RequestBedData:
    """
    Attributes
    __________
    panel_info : dict
        A dictionary created by panelapp_requests.py containing information
        about the panel in question.
    gene_list : list
        A list of genes taken form panel_info.
    reference_genome : str
        The reference genome given as an argument option at program start.
    base_url : str
        The base URL for variant validator.
    gene_dict : dict
        Uses private method to cycle through the genes in gene_list and
        returns nested API responses as dictionaries per gene.

    Methods
    _______
    __get_responses()
        Performs an API request to Variant Validator on a list of genes and
        returns the responses as nested dictionaries per gene.
    create_bed_file()
        Gathers all the relevant information from the API responses to create
        the bed file line by line. Currently outputs to a hardcoded location,
        but this will change in the future.
    """
    def __init__(self, ref_genome, panel_info):
        self.panel_info = panel_info
        self.gene_list = panel_info["genes"]
        self.reference_genome = ref_genome
        self.base_url = "https://rest.variantvalidator.org/"
        self.gene_dict = self.__get_responses()


    def __get_responses(self):
        gene_dict = {}
        for gene in self.gene_list:
            url = f"/VariantValidator/tools/gene2transcripts_v2/\
                    {gene}/mane/all/{self.reference_genome}"
            try:
                response = requests.get(self.base_url + url, 
                                        headers={"Content-Type": 
                                                "application/json"},
                                        timeout=30
                                        )
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print('HTTP Error: Variant Validator does not recognise url')
                log.error(errh.args[0])
                sys.exit(1)
            except requests.exceptions.ReadTimeout as errt:
                print("Error: Time out on Variant Validator API request")
                log.error(errt.args[0])
                sys.exit(1)
            except requests.exceptions.ConnectionError as conerr:
                print("Connection Error: No internet connection")
                log.error(conerr.args[0])
                sys.exit(1)
            # Append response to gene_dict using gene from gene_list as the
            # key
            gene_dict["{}".format(gene)] = response.json()

        return gene_dict
    
    def create_bed_file(self):
        # Create output bed file name from identifying factors
        # output_dir to change from being hardcoded
        output_dir = "bed_repository/"
        r_code = self.panel_info["r_number"]
        panel_version = self.panel_info["panel_version"]
        refno = self.reference_genome[0]
        output_file = f"{output_dir}{r_code}_GCRh{refno}_V{panel_version}.bed"

        # Create the output file and append headers
        with open(output_file, "w") as file:
            file.write(f"#REFERENCE GENOME BUILD: GRCh{refno}\n")
            file.write("".join(["#GENE\t #SYMBOL\t #TRANSCRIPT\t #GENOMIC ",
                                "SPAN\t #CHROMO\t #EXON\t #START\t #END\n"]))
        
        # Gather relevant information for bed file from API responses per gene
        for gene, transcript in self.gene_dict.items():
            chromosome = transcript[0]["transcripts"][0]["annotations"]\
            ["chromosome"]
            gene_symbol = transcript[0]["current_symbol"]
            hgnc = transcript[0]["hgnc"]
            transcript_id = transcript[0]["transcripts"][0]["reference"]

            with open(output_file, "a") as file:
                for genomic_span_key, genomic_span_value in transcript[0]\
                    ["transcripts"][0]["genomic_spans"].items():
                    for exon in genomic_span_value["exon_structure"]:
                        exon_number = exon["exon_number"]
                        start = int(exon["genomic_start"])-30
                        end = int(exon["genomic_end"])+10
                        file.write('\t'.join([gene_symbol, hgnc, transcript_id,
                                              genomic_span_key,
                                            "chr" + str(chromosome), 
                                            str(exon_number), str(start), 
                                            str(end), "\n"
                                    ]))
