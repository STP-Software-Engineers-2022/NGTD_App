'''############################################################################
Command Line Interface
############################################################################'''

import argparse

class cli_obj():

    def __init__(self, sys_args):
        parser = argparse.ArgumentParser(description='')

        parser.add_argument(
            '-r', '--r_number', required = True, help = 'Provide the R number \
                from the National Genomic Test Directory.')
        parser.add_argument(
            '-f', '--file', action='store_true',
            help='A txt file containing a list of R numbers. Gene list \
                returned will remove duplicates.')
        parser.add_argument(
            '-e', '--example', action='store_true',
            help='Empty.')
        
        self.args = parser.parse_args(sys_args)

    def arg_selection(self):
        selected = [False, False]
        if (self.args.example == True):
            selected[0] = True
        if (self.args.example2 == True):
            selected[1] = True
        return selected