"""
Generate a bed file for a gene panel
Authors: D. Scales, N. Gallop
Last updated: Carline Riehl - 21-Jan-2024
"""
from config import log
import requests
import sys
import os


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
    output_dir : str
        The repository of bed files held locally to save any new bed files to
    gene_dict : dict
        Uses private method to cycle through the genes in gene_list and
        returns nested API responses as dictionaries per gene. Empty attribute
        until initialisation of instance.

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
        self.output_dir = "bed_repository/"
        self.gene_dict = None
        self.__get_responses()


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
                error = "HTTP Error: Variant Validator does not recognise url"
                log.error(errh.args[0])
                sys.exit(error)
            except requests.exceptions.ReadTimeout as errt:
                error = "Error: Time out on Variant Validator API request"
                log.error(errt.args[0])
                sys.exit(error)
            except requests.exceptions.ConnectionError as conerr:
                error = "Connection Error: No internet connection"
                log.error(conerr.args[0])
                sys.exit(error)
            # Append response to gene_dict using gene from gene_list as the
            # key
            log.debug("API successfully called in create_beds.py")
            gene_dict["{}".format(gene)] = response.json()

        self.gene_dict = gene_dict
        return True
    
    def create_bed_file(self):
        # Create output bed file name from identifying factors
        output_dir = self.output_dir
        r_code = self.panel_info["r_number"]
        panel_version = self.panel_info["panel_version"]
        refno = self.reference_genome[0]
        output_file = f"{output_dir}{r_code}_GRCh{refno}_V{panel_version}.bed"
        
        if os.path.isfile(output_file):
            debug_message = "BED file for this gene panel (inc. ref genome "\
                "and panel version) already exists - nothing new written."
            print(debug_message)
            log.debug(debug_message)
            
        else:
            try:
                # Create the output file and append headers
                self.create_file(output_file, refno)
                # Gather relevant information for bed file from API responses per gene
                self.write_file(output_file)
            except:
                error = "Could not create bed file, process aborted."
                log.error(error)
                sys.exit(error)
            log.debug("Successfully created bed file")

        return output_file

    def create_file(self, file_name, ref_genome_build):
        with open(file_name, "w") as file:
            file.write(f"#REFERENCE GENOME BUILD: GRCh{ref_genome_build}\n")
            file.write("".join(["#GENE\t #SYMBOL\t #TRANSCRIPT\t #GENOMIC ",
                                "SPAN\t #CHROMO\t #EXON\t #START\t #END\n"]))
        return True
    
    def write_file(self, file_name):
        log.debug(f"Writing bed file for {file_name}")
        for gene, transcript in self.gene_dict.items():
            chromosome = transcript[0]["transcripts"][0]["annotations"]\
            ["chromosome"]
            gene_symbol = transcript[0]["current_symbol"]
            hgnc = transcript[0]["hgnc"]
            transcript_id = transcript[0]["transcripts"][0]["reference"]

            with open(file_name, "a") as file:
                for genomic_span_key, genomic_span_value in transcript[0]\
                    ["transcripts"][0]["genomic_spans"].items():
                    for exon in genomic_span_value["exon_structure"]:
                        exon_number = exon["exon_number"]
                        start = int(exon["genomic_start"])-30
                        end = int(exon["genomic_end"])+10
                        file.write("\t".join([gene_symbol, hgnc, transcript_id,
                                              genomic_span_key,
                                            "chr" + str(chromosome), 
                                            str(exon_number), str(start), 
                                            str(end), "\n"
                                    ]))
            log.debug(f"Info for {gene} added to bed file")
        return True
