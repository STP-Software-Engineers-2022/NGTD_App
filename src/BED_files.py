'''
Generate a bed file for a gene panel
'''
from config import log
import requests
import sys


class request_data():

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
                                        timeout=5
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
            gene_dict["{}".format(gene)] = response.json()

        return gene_dict
    
    def create_bed_file(self):
        r_number = self.panel_info["r_number"]
        panel_version = self.panel_info["panel_version"]
        refno = self.reference_genome[0]
        output_file = f"output/{r_number}_GCRh{refno}_V{panel_version}.bed"
        ref_seq = self.reference_genome[0]
        with open(output_file, "w") as file:
            file.write(f"#REFERENCE GENOME BUILD: GRCh{ref_seq}\n")
            file.write("".join(["#GENE\t #SYMBOL\t #TRANSCRIPT\t #GENOMIC ",
                                "SPAN\t #CHROMO\t #EXON\t #START\t #END\n"]))
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