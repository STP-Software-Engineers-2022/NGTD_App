'''
Workflow manager for running program
'''
import sys
import src.command_line_interface as cli
import src.panelapp_requests as pan
import src.get_directory as get_dir
import src.data_import as data_import
import src.create_beds as bed
from config import log

def main(argv=None):
    
    # initialise cli object
    parsed = cli.CommandLineInterface(sys.argv[1:])
    args = parsed.args
    if args.download_directory is not None:
        ngtd_dir = get_dir.get_directory(args)
        ngtd_dir.download_doc()
    # Create an instance of MyRequests
    my_requests = pan.MyRequests(args)
    
    # Make the API request
    response = my_requests.request_data()
    gene_list, signoff = my_requests.gene_list(response)
    my_requests.print_info(response, args, gene_list, signoff)

    if args.create_bed:
        panel_info = my_requests.database_postage(response)

        gene_panel_transcripts = bed.RequestBedData(
            parsed.ref_genome, panel_info)
        bed_file_link = gene_panel_transcripts.create_bed_file()

        # Import panel information (test and genes) and bed file into database
        data_import.main(panel_info, bed_file_link)
    
    else:
        print("No panel information added to the database. Run with -b to add the data.")

    return True

if __name__ == "__main__":
    if main():
        to_log = 'main.py ran successfully'
        print(f"\nLogging: {to_log}")
        log.info(to_log)
