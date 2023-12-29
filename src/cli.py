'''############################################################################
Command Line Interface
############################################################################'''

import argparse

class cli_obj():

    def __init__(self, sys_args):
        parser = argparse.ArgumentParser(description='')

        parser.add_argument(
            '-r', '--r_number', required = True, 
            help = 'Provide the R number \
                from the National Genomic Test Directory.')
        parser.add_argument(
            '-b', '--bed', required = False, action='store_true',
            help = 'Generate a bed file and record your query.')
        parser.add_argument(
            '-g', '--get_doc', required = False, \
            action='store_true',
            help='Download the National Genomic Test Directory document.')
        parser.add_argument(
            '-o', '--output', required = False, \
            help='Specify the path for your output e.g. for test directory \
                document or bed file.')
        parser.add_argument(
            '-f', '--file', action='store_true',
            help='A txt file containing a list of R numbers. Gene list \
                returned will remove duplicates.')
        
        self.args = parser.parse_args(sys_args)
