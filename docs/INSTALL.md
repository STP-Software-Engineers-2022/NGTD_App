# Installation
Date created: 24-Jan-2024
Date modified: 24-Jan-2024
Authors: Danni Scales

This document provides instructions for installing the National Genomic Test Directory (NGTD) application and accompanying database on Mac OS X and Linux Ubuntu computers. We recommend installing locally by downloading the [installing through Docker](#install-through-docker) for all other systems, or if you encounter any installation issues.

## Pre-requisites
Required:
 - [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
 - Local install: Anaconda or [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
 - Container install: [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) (Linux) or [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac OS)



## Download the source code
If you havent already, please download the appropriate version of [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) for your OS before proceeding.

In your terminal, clone the NGTD repository from GitHub.com onto your local machine::
```
git clone https://github.com/STP-Software-Engineers-2022/NGTD_App.git
```
Then navigate into the NGTD_App directory:
```
cd NGTD_App
```

## Local Install
### Create a virtual environment
When installing the NGTD app, a python environment should be created to install the specific versions of dependencies needed for the package to run.

If you havent already, please download the appropriate version of [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) for your OS before proceeding.

1. Create a conda [environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) from the ```environment.yml``` file, which specifies the dependencies required for the application to run: 
```
conda env create -f environment.yml
```

2. Activate the environment:
```
conda activate ngtd
```

### Install the NGTD app
1. Use ```pip``` to install the ```pyproject.toml``` file into the current directory, which contains the build system requirements for the application:
```
pip install .
```
2. Verify that NGTD app has been successfully installed:
```
python main.py --help
```
The installation has been successful if you are presented with the following output:
```
usage: main.py [-h] [-g] [-b] [-r R_NUMBER] [-d [DOWNLOAD_DIRECTORY]]

optional arguments:
  -h, --help            show this help message and exit
  -g, --gene_list       Return a list of gene from a gene panel for a given R
                        number
  -b, --create_bed      Generate a bed file for a given gene list
  -r R_NUMBER, --r_number R_NUMBER
                        Provide the R number from the Genomic Test Directory
                        that you wish to enquire about
  -d [DOWNLOAD_DIRECTORY], --download_directory [DOWNLOAD_DIRECTORY]
                        Download the latest national test directory and save.
                        Please input an output location, default output to
                        docs directory
```
If there are any issues with the pyproject.toml installation, the appropriate dependencies can be added via:
```
pip install -r docs/requirements.txt
```
---
## Install through Docker
### For Linux Ubuntu
1. If you haven't already, please download and install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

2. Build a Docker image from the Dockerfile, which is located in the current directory. The ```--tag``` (```-t```) flag is used to name the Docker image: 
```
sudo docker build -t ngtd .
```

3. Run the application in a Docker container, specifying the image reference to create the container:
```
sudo docker run -it ngtd --help
```
The installation has been successful if you are presented with the following output:
```
usage: main.py [-h] [-g] [-b] [-r R_NUMBER] [-d [DOWNLOAD_DIRECTORY]]

optional arguments:
  -h, --help            show this help message and exit
  -g, --gene_list       Return a list of gene from a gene panel for a given R
                        number
  -b, --create_bed      Generate a bed file for a given gene list
  -r R_NUMBER, --r_number R_NUMBER
                        Provide the R number from the Genomic Test Directory
                        that you wish to enquire about
  -d [DOWNLOAD_DIRECTORY], --download_directory [DOWNLOAD_DIRECTORY]
                        Download the latest national test directory and save.
                        Please input an output location, default output to
                        docs directory
```

### For Mac OS
1. If you havent already, please download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/) 

2. In the command line, launch the Docker daemon using Docker Desktop:
```
open -a Docker
```

3. Build a Docker image from the Dockerfile, which is located in the current directory. The ```--tag``` (```-t```) flag is used to name the Docker image: 
```
docker build -t ngtd .
```

4. Run the application in a Docker container, specifying the image reference to create the container:
```
docker run -it ngtd --help
```
The installation has been successful if you are presented with the following output:
```
usage: main.py [-h] [-g] [-b] [-r R_NUMBER] [-d [DOWNLOAD_DIRECTORY]]

optional arguments:
  -h, --help            show this help message and exit
  -g, --gene_list       Return a list of gene from a gene panel for a given R
                        number
  -b, --create_bed      Generate a bed file for a given gene list
  -r R_NUMBER, --r_number R_NUMBER
                        Provide the R number from the Genomic Test Directory
                        that you wish to enquire about
  -d [DOWNLOAD_DIRECTORY], --download_directory [DOWNLOAD_DIRECTORY]
                        Download the latest national test directory and save.
                        Please input an output location, default output to
                        docs directory
```
