'''############################################################################
Purpose: For testing objects
Date: 07/11/2023
############################################################################'''
import sys
import src.cli as cli

def main():

    # initialise cli object
    cli_obj = cli.cli_obj(sys.argv[1:])
    selected_args = cli_obj.arg_selection()
    # check if arguments have been selected and abort program if not
    if selected_args == [False, False]:
        print("No arguments selected, aborting program")
        quit()
    
    r_code = cli_obj.args.r_number
    print(r_code)


if __name__ == "__main__":
    main()