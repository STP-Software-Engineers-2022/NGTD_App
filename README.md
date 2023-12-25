
# README.md
## NGTD_App as part of STP Software Engineering Module
###### Date created: 2023-11-07
###### Date modified: 2023-11-14
###### Authors: Dolapo Ajayi, Niall Gallop, Caroline Riehl, Danni Scales

## Overview
A tool to manage gene panels for NHS National genomic test directory tests in the laboratory

### Project Aims:
1. Find relevant gene panel for a genomic test to assist analysis of sequence data
    - Use PanelApp API to retrieve gene list of a gene panel based on a given R number
    - Expand this functiaonlity to accept a list of R numbers
    - Investigate expanding functionality to accept more than just R numbers

2. Generate a BED file from a gene panel that can be used an an input for an NGS pipeline

3. Build a safe and efficient repository of genetic test and panel information
    - For use in the laboratory 
    - Emphasis on reliability and speed

4. Build a repository of which tests, gene panels, BED files, reference sequences and version which have been applied to each patient case so that the laboratory has an accurate record of how analyses were performed.

## Gitflow
### Generic Gitflow
![Alt text](docs/generic_gitflow.png?raw=true)

### Our Gitflow
Updated: 10/11/2023
![Alt text](docs/project_gitflow.png?raw=true)

## Download Details and Conda Env Creation
```
git clone https://github.com/STP-Software-Engineers-2022/NGTD_App.git
cd NGTD_App
conda env create -f environment.yml
conda activate ngtd
pip install -r requirements.txt
```

## Run Script
Script currently in development. 
Currently run as follows. [arg] is a valid R number from National Genomic Test Directory
```
# 1. For list of genes relating to a panel to be printed on the command line:
python3 main.py -g -r [arg]
```
```
# 2. For the panel information (panel, genes list) and the bed file to be added to the database:
python3 main.py -g -r [arg] -b
# Input when prompted the version of the reference genome for which to create the bed file.
```


## Database
*For development*
If required, an empty database can be re-created by running the database.py script from the NGTD_App directory. Make sure to delete the database first.
```
python3 src/database.py
```

TODO: add logs
TODO2: add unit tests


## Testing
```
pytest
```