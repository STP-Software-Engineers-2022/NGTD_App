'''############################################################################
Command Line Interface
############################################################################'''

import argparse

class cli_obj():

    def __init__(self, sys_args):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            "--subproc", action='store_true', 
            help="Please select the program requirements."
        )
        parser.add_argument(
            '-g', '--get_doc', required = False, \
            action='store_true',
            help='Download the National Genomic Test Directory document.')
        subparsers = parser.add_subparsers()

        # Return gene list function
        parser_gene_list = subparsers.add_parser(
            'gene_list', help='Provide a valid R number from the National '
            'Genomic Test directory and have a list of gene sassociated with '
            'the gene panel returned.'
            )
        parser_gene_list.add_argument(
            '-r', '--r_number', required = True, 
            help = 'Provide the R number \
                from the National Genomic Test Directory.')
        
        # Create BED file function
        parser_create_bed = subparsers.add_parser(
            'create_bed', help='Create a BED file from a given gene and '
            'reference genome'
            )
        parser_create_bed.add_argument(
            '-g', '--gene',
            help = 'Name of the gene')
        parser_create_bed.add_argument(
            '-r', '--reference_genome',
            help='')
        parser_create_bed.add_argument(
            '-o', '--output',
            help='Specify the path for your output e.g. for test directory '
                'document or bed file.')

        
        self.args = parser.parse_args(sys_args)


class cli_obj_from_bed():

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
