# NGTD_App
### As part of the STP Software Engineering Module at the University of Manchester
Date created: 07-Nov-2023  
Date modified: 26-Jan-2024  
Authors: Dolapo Ajayi, Niall Gallop, Caroline Riehl, Danni Scales  

The NGTD app is a tool to manage gene panels for [NHS National Genomic Test Directory](https://www.england.nhs.uk/publication/national-genomic-test-directories/) tests in the laboratory

The most recent documentation build for the NGTD app can be found [here](https://ngtd-app-ngtd-app.readthedocs-hosted.com/en/latest/)

# Assessor Documentation
This document is designed to elaborate upon some of the decisions that were made during the development of the project, why we made those decisions, and the impact they've had on the project.

While this kind of documentation is not normal for a piece of software, we felt it would be useful for the assessor to have some things pointed out, rather than expect them to figure it out by scrolling through weeks of commit history. We discussed this with the stakeholders (Pete and Andrew) and it was agreed that it would be a useful addition.

# Git Practice
Version control, Git, and GitHub were new to the whole group and therefore this aspect of the project developed over time. Some mistakes were made (detailed below) but were handled as realistically and as effectively as we could.

## GitHub "Organisation"
During the on-campus week in November when we started the project, the first thing to do was create the repository. A member of the team set up an organisation, invited the group to the organisation and then created the repository. At the time, we did not understand the consequences of this - being severely limited gitHub tools without the "organisation" paying for a premium GitHub package. This resulted in us being unable to use "Insights" tools, and prevented us from properly protecting the main branch. We noticed this too late to change.

## Main push
On December 29th 2023, an accidental commit was made to the 'main' branch, carrying with it commits dating back to the start of the project. An attempt was made to immediately revert the commit, but this was unsuccessful. We consulted the stakeholders and agreed that, as 'main' was not a deployed branch, there were no consequences of this accidental commits. These changes were overwritten by the eventual merge of the release branch at the end fo the project.

## Code Review
The early stages of the project, Pull Requests were merged without code review into 'dev'. However, particularly when the quantity of work being produced went up, code reviews became more necessary. This was something we introduced later on as we understood more about this practice.

## Project Kanban Board
We opted to use the Github feature 'Project' to organise our issues into sprints and assign them. Please view the project tab from the repository to see the way we organised the work.

# Program Decisions
## Use of src/
Many online resources state that for simple python projects, the best format is to have a main executable file in the root directory of the project, with all other source code stored in a subdirectory called 'src/'. This convention is also followed by our workplaces, except for larger packaged programs. 

Following a discussion as a group about this, we decided to maintain this structure as we felt it was most applicable to the scale of the project. the other option we considered was moving the main script to a 'bin/' subdirectory and housing all the other source code in a subdirectory named after the program. This format is more suitable to larger, packaged programs but seemed overly complicated for this project.

## `requirements.txt` and `pyproject.toml`
Many online resources agree that the `pyproject.toml` file should be used to replace the `setup.py` file, rather than replace the `requirements.txt` file as stated in the rubric; leaving the `pyproject.toml` file to broadly outline dependencies and the `requirements.txt` file to lock down the versions. To reduce complications, we decided to separate the installation into two primary methods:  
1. A 'local' install using conda and pip to install from a `environment.yml` and `pyproject.toml` which still includes reference to the python packages in the `requirements.txt`.  
2. A 'container' install using Docker. The Dockerfile includes reference to the python packages in the `requirements.txt`.

## Use of `main.py` nomenclature
`main.py` was used an an initial placeholder main script file to be executed. However, this stuck around too long and became embedded in the documentation. 

## Populated Database
Following a meeting with stakeholders (Pete and Andrew) they requested a database be provided, populated with dummy data for demonstration purposes. The ngtd.db database in the repository is therefore there to fulfill that purpose. Under normal circumstances, it would not be included and the database should initialise during the first run.

# Technical Details
## Linux OS details
Project was developed on Mac OS >= 12.3
 - >= 12.3, Intel
 - >= 13.6.3 Apple Silicon

Project has been tested on a Linux virtual machine:
 - Ubuntu 22.04.3 (LTS)
 - x86-64 architecture
 - Kernel: Linux 6.5.0-14-generic

## Outstanding Issues
Outstanding Issues are logged in github - the easiest way to view the issues closed vs the issues outstanding it to view the Github Project Kanban board.

Primarily, the requested jenkinsfile is issued for a later sprint but is not a part of this minimal viable product.

### Bugs
We detected a bug in the program when some valid R numbers are passed to the program. This bug is issued (42) for a later sprint. We have not been able to develop a comprehensive list of R numbers that are affected but we have noticed it with R444 and R419.  
 - R444: Returns that the panel doesn't exists according to panelapp_requests  
 - R419: Fails with -b during bed file creation. A large bed file is written, but the writing process fails to complete resulting in the program terminating through a sys.exit(). The resulting bed file is not posted to the database as it should be.  