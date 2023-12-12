
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
Script currently in development. Currently run via:
```
# [arg] is a valid R number from National Genomic Test Directory
python main.py -r [arg]
```

## Database
*For development*
1. If required, an empty database be re-created by running the database.py script from the NGTD_App directory.
```
python3 src/database.py
```

2. Panel/test information will be stored in the database when using the following command:
```
python3 main.py -r <R code> -b
```

TODO: add functionality to add bed file into database as well
TODO2: add logs


## Testing
```
pytest
```