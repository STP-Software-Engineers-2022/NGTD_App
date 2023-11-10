
# README.md
## NGTD_App as part of STP Software Engineering Module
###### Date created: 2023-11-07
###### Date modified: 2023-11-07
###### Authors: danniscales, DolapoA, NGallop

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
```xml

```
### Our Gitflow
Updated: 10/11/2023
```xml
<mxfile host="app.diagrams.net" modified="2023-11-10T14:47:27.430Z" agent="5.0 (Macintosh)" etag="2XyGB6Y12sBWC8tho4kP" version="21.0.6" type="device">
    <diagram id="yPxyJZ8AM_hMuL3Unpa9" name="simple gitflow">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</diagram>
</mxfile>
```
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
python main.py [arg]
```

## Testing
```
pytest
```