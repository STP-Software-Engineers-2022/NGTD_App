"""
The workflow manager module for running panel request program.

Functions
---------
main(argv=None)
    Handles the execution of the entire application based on command 
    line arguments.
"""
import sys
import src.command_line_interface as cli
import src.panelapp_requests as pan
import src.get_directory as get_dir
import src.data_import as data_import
import src.create_beds as bed
from config import log

def main(argv=None):
    """
    Executes the core method of the application based on command line 
    arguments recieved from the user.

    It initializes the command line interface, processes arguments,
    and executes actions accordingly, such as like downloading documents, 
    making API requests, creating BED files, and importing data into a 
    database. It handles the flow of the application and ensures the 
    execution of tasks based on user input.

    Parameters
    ----------
    argv : list of str, optional
        A list of command line arguments. Defaults to None, which uses 
        sys.argv.

    Returns
    -------
    boolean
        True if the execution was successful, False otherwise.

    Notes
    -----
    - The function exits the program with an error message if required
      arguments are not provided.
    - Logs the successful completion of the script.
    """

    # initialise cli object
    parsed = cli.CommandLineInterface(sys.argv[1:])
    args = parsed.args
    if args.download_directory is not None:
        ngtd_dir = get_dir.GetDirectory(args)
        ngtd_dir.download_doc()
    
    if args.r_number is None:
        return True
    
    # Create an instance of MyRequests

    my_requests = pan.MyRequests(args)

    
    # Make the API request
    response = my_requests.request_data()
    gene_list, signoff = my_requests.gene_list(response)
    if args.gene_list:
        my_requests.print_info(response, args, gene_list, signoff)
    else:
        pass
        

    if args.create_bed:
        panel_info = my_requests.database_postage(response)

        gene_panel_transcripts = bed.RequestBedData(
            parsed.ref_genome, panel_info)
        bed_file_link = gene_panel_transcripts.create_bed_file()

        # Import panel information and bed file path into database
        data_import.import_into_database(panel_info, bed_file_link)
    
    else:
        msg = "No panel information added to the database. "\
            "Run with -b to add the data."
        log.info(msg)
        print(msg)

    return True

if __name__ == "__main__":
    if main():
        to_log = "main.py ran successfully"
        log.info(to_log)
