'''############################################################################
Purpose: For testing objects
Date: 07/11/2023
############################################################################'''
import sys
import src.cli as cli
import src.panelapp_requests as pan
from config import log

def main(argv=None):
    
    # initialise cli object
    cli_obj = cli.cli_obj(sys.argv[1:])
    r_code = cli_obj.args.r_number

    # Create an instance of MyRequests
    my_requests = pan.MyRequests(r_code)

    # Make the API request
    response = my_requests.request_data()
    my_requests.print_info(response, r_code)
    
    to_log = 'Example_log'
    print(f"Logging: {to_log}")
    log.info(to_log)

    return True

if __name__ == "__main__":
    main()