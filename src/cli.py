'''
Command Line Interface
'''

import argparse
import sys

class cli_args():

    def __init__(self, sys_args):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-g", "--gene_list", action="store_true", 
            help="Return a list of gene from a gene panel for a given \
                R number"
        )
        parser.add_argument(
            "-b", "--create_bed", action="store_true",
            help="Generate a bed file for a given gene list"
        )
        parser.add_argument(
            "-r", "--r_number",
            help="Provide the R number from the Genomic Test Directory that \
                you wish to enquire about"
        )
        parser.add_argument(
            "-d", "--download_directory", nargs="?", const="docs/", 
            default=None,
            help="Download the latest national test directory and save. \
                Please input an output location, default output to docs \
                directory"
        )

        self.args = parser.parse_args(sys_args)
        self.ref_genome = None
        self.__handle_options()

    def __arg_selection(self):
        selected = [False, False, False, False]
        if (self.args.gene_list == True):
            selected[0] = True
        if (self.args.create_bed == True):
            selected[1] = True
        if (self.args.r_number is not None):
            selected[2] = True
        if (self.args.download_directory is not None):
            selected[3] = True
        return selected

    def __handle_options(self):
        selected_args = self.__arg_selection()

        if selected_args[0] == True:
            if selected_args[2] != True:
                print("If gene_list is selected, an R number must be given",
                      "with flag -r"
                      )
                sys.exit()
        if selected_args[1] == True:
            if selected_args[2] != True:
                print("If bed file creation selected, an R number must be",
                      " passed with flag -r"
                      )
                sys.exit()
            else:
                while True:
                    ref_genome = input(" ".join(["For which reference genome",
                                        "should the bed file be created?",
                                        "[37/38]"])
                                        )
                    if ref_genome == "37":
                        self.ref_genome = ["37"]
                        break
                    elif ref_genome == "38":
                        self.ref_genome = ["38"]
                        break
                    else:
                        print("Please enter 37 or 38")
                        continue

        if list(selected_args[i] for i in [0,1,3]) == [False, False, False]:
            print("Error: Must select at least one of the following options:",
                  "\"--gene_list\", \"--create_bed\", \"--download_directory\"")
            sys.exit()

        return True