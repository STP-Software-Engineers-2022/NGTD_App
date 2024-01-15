
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

### Early Gitflow
Updated: 10/11/2023
![Alt text](docs/project_gitflow.png?raw=true)

## Running the Program
#### To download and run locally:
Conda must be installed to run this program locally. Instructions for installatino of Anaconda can be found here: https://www.anaconda.com/

Download and install:
```
git clone https://github.com/STP-Software-Engineers-2022/NGTD_App.git
cd NGTD_App
conda env create -f environment.yml
conda activate ngtd
pip install -r requirements.txt
```

Run Script:
Script currently in development. Currently run via:
```
python main.py [ARGS]
```

#### To download and run from container:
Docker must be installed to to this program via a container. Docker must be open in the background to build and activate the container. Download instructions for Docker can be found here: https://www.docker.com/products/docker-desktop/

Download:
```
git clone https://github.com/STP-Software-Engineers-2022/NGTD_App.git
cd NGTD_App
```

Build and run program from container:
```
docker build -t ngtd .
docker run ngtd [ARGS]
```

#### Arguments

For information on args, use -h or see below:
```
usage: main.py [-h] [-g] [-b] [-r R_NUMBER] [-d [DOWNLOAD_DIRECTORY]]

options:
  -h, --help            show this help message and exit
  -g, --gene_list       Return a list of gene from a gene panel for a given R number
  -b, --create_bed      Generate a bed file for a given gene list
  -r R_NUMBER, --r_number R_NUMBER
                        Provide the R number from the Genomic Test Directory that you wish to enquire about
  -d [DOWNLOAD_DIRECTORY], --download_directory [DOWNLOAD_DIRECTORY]
                        Download the latest national test directory and save. Please input an output location, default output to docs directory
```

## Testing
Pytest can be run from inside the program root using the following command in the terminal:

```
pytest
```