# Installation
This document provides instructions for installing the National Genomic Test Directory (NGTD) app across all Operating Systems (OS) (ie. Linux, Mac and Windows)

If you havent already, please download the appropriate versions of [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) for your OS before proceeding.

In your terminal, clone the NGTD repository from GitHub.com onto your local machine. This will ensure you have a complete version history of all the files and folders associated with this project:
```
git clone https://github.com/STP-Software-Engineers-2022/NGTD_App.git
```
Then navigate into the NGTD_App directory:
```
cd NGTD_App
```

## Installation options
There are then three different ways install the NGTD app and all required dependencies:

1. Install using requirements.txt and environment.yml
2. Install using pyproject.toml
3. Install using Docker container

### 1. Install using requirements.txt and environment.yml
1. Create a conda [environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) from the ```environment.yml``` file, which specifies the python packages and versions required for the project to run: 
```
conda env create -f environment.yml
```

2. Activate the environment:
```
conda activate ngtd
```

3. Use ```pip``` to install the ```requirements.txt``` file, which specifies the dependencies required for the project to run. The ```--requirements``` (```-r```) flag is used to indicate the requirements filename:
```
pip install -r requirements.txt
```

4. Verify that NGTD app has been successfully installed:
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

### 2. Install using pyproject.toml
1. Use ```pip``` to install the ```pyproject.toml``` file, containing the build system requirements for the project, into the current directory:
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

### 3. Install using docker container
1. If you havent already, please download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/) 

2. In the command line, launch the docker daemon using Docker Desktop:
```
open -a Docker
```

3. Build a Docker image from the Dockerfile, which is located in the current directory. The ```--tag``` (```-t```) flag is used to name the Docker image: 
```
docker build -t ngtd .
```

4. Run the application in a Docker container, specifying the image reference to create the container:
```
docker run ngtd python main.py --help
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