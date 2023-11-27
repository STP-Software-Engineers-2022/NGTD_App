'''############################################################################
Purpose: For testing objects
Date: 07/11/2023
############################################################################'''
import sys
import src.cli as cli
import src.panelapp_requests as pan
import src.get_directory as get_dir
from config import log
from config import td_url as url

def main(argv=None):
    
    # initialise cli object
    cli_obj = cli.cli_obj(sys.argv[1:])
    r_code = cli_obj.args.r_number
    bed = cli_obj.args.bed
    get_doc = cli_obj.args.get_doc
    output =  cli_obj.args.output

    # Create an instance of MyRequests
    my_requests = pan.MyRequests(r_code)

    # Make the API request
    response = my_requests.request_data()
    gene_list, signoff = my_requests.gene_list(response)
    my_requests.print_info(response, r_code, gene_list, signoff)

    # Prepare data for database deposition
    my_requests.database_postage(response, r_code, bed, gene_list, signoff)

    ngtd_dir = get_dir.get_directory()
    ngtd_dir.download_doc(get_doc, output, url)

    to_log = 'main.py ran successfully'
    print(f"\nLogging: {to_log}")
    log.info(to_log)

    return True

if __name__ == "__main__":
    main()