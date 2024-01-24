"""
The Command Line Interface module handles command line arguments for 
gene panel data processing.

Author: N. Gallop
"""

import argparse
import sys

class CommandLineInterface:
    """
    A class for handling command line arguments for working with gene panel 
    data.
    
    Attributes
    __________
    args : Namespace
        Arguments parsed from sys args.
    ref_genome : str
        Reference genome if required based on argument selection.
    
    Methods
    _______
    __arg_selection()
        Creates a list positionally relational to argument options to help
        with handling the options.
    __handle_options()
        Uses arg_selection boolean list to handle argument conflicts, lacking
        arg information or to ask the user to more information.
    """
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
        """
        Determine which command line arguments were selected.

        This method returns a list of boolean values corresponding to the selection
        state of each command line argument.

        Returns
        -------
        list of boolean
            List indicating which arguments were selected.
        """
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
        """
        This method is responsible for command line arguments, 
        it checks for conflicts and prompts for additional information 
        if necessary.

        It uses the list of selected arguments from __arg_selection() method
        to validate argument combinations and ask the user for any
        further required information.

        Returns
        -------
        bool
            True if the arguments were handled successfully, False otherwise.

        Exits
        -----
        The method exits the program if there are argument conflicts or if
        necessary information is missing.
        """
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
                  "\"--gene_list\", \"--create_bed\",",
                   "\"--download_directory\"")
            sys.exit()

        return True
        